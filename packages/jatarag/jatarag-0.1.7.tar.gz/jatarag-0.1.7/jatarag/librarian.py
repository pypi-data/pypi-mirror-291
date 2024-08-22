from __future__ import annotations

import re
from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Literal, Generator, get_args, overload

from .db import Database, ParagraphResult, MetadataResult
from .agent import Agent, Message, Role
from .utils import strip_quotes


@overload
def synthesize_answer(agent: Agent, query: str, paragraphs: list[str], stream: Literal[False], chat_history: list[Message] = []) -> str: ...
@overload
def synthesize_answer(agent: Agent, query: str, paragraphs: list[str], stream: Literal[True], chat_history: list[Message] = []) -> Generator[str, None, None]: ...
def synthesize_answer(agent: Agent, query: str, paragraphs: list[str], stream: bool, chat_history: list[Message] = []) -> str | Generator[str, None, None]:
    """
    Synthesize an answer to a RAG query based on the given paragraphs

    Parameters:
        agent (Agent): the agent to use to synthesize the answer
        query (str): the original user query
        paragraphs (list[str]): the paragraphs to use as context. Should be relevant for answering the query
        stream (bool, optional): whether to stream the answer or not. If False, returns a single string, Otherwise returns a generator.
        chat_history (list[Message], optional): the chat history to use as context. Defaults to []

    Returns:
        str | Generator[str, None, None]: the synthesized answer. Setting stream=True will return a generator, otherwise a string
    """

    # use agent to answer the question based on the results
    prompt = "You are a librarian. Users will ask you questions, and you should answer based on relevant snippets of the documents available. Your library database will automatically provide you with possibly relevant snippets. Please cite phrases/sentences in your answer with the number(s) of the relevant snippet(s) (e.g. [5], or [6][7][13])"
    context = "\n\n".join([f"[{i}]: {paragraph}" for i, paragraph in enumerate(paragraphs)])
    query = f'user query:"{query}"\n\nrelevant document snippets:\n{context}\n\nyour answer: '

    messages = [
        Message(role=Role.system, content=prompt),
        *chat_history,
        Message(role=Role.user, content=query)
    ]

    if stream:
        answer = agent.multishot_streaming(messages)
    else:
        answer = agent.multishot_sync(messages)

    return answer


@dataclass
class Query:
    target: Literal['query_titles', 'query_authors', 'query_publishers', 'query_document', 'query_whole_database']
    query: str
    arg: str | None = None

    def __post_init__(self):
        # Ensure that target is one of the valid options
        try:
            # normal case where annotations are available
            target_options = Query.__annotations__['target'].__args__
        except AttributeError:
            # hacky way to handle from __future__ import annotations.
            # `eval` should be safe here because it's input argument comes directly from the source of this file
            target_options = get_args(eval(Query.__annotations__['target']))

        assert self.target in target_options, f'Invalid query target: "{self.target}". Must be one of {target_options}'

    def __str__(self):
        if self.arg is not None:
            return f'{self.target}({self.arg}): {self.query}'
        return f'{self.target}: {self.query}'


class RagAgent(ABC):
    @overload
    def ask(self, query: str, *, stream: Literal[False], max_results: int) -> tuple[list[ParagraphResult], str]: ...
    @overload
    def ask(self, query: str, *, stream: Literal[True], max_results: int) -> tuple[list[ParagraphResult], Generator[str, None, None]]: ...
    @abstractmethod
    def ask(self, query: str, *, stream: bool, max_results: int) -> tuple[list[ParagraphResult], str | Generator[str, None, None]]:
        ...


class SimpleRagAgent(RagAgent):
    def __init__(self, db: Database, agent: Agent):
        """
        Create a simple RAG Agent that does not maintain conversation history

        Args:
            db (Database): the database to query
            agent (Agent): the agent to use for answering questions
        """
        self.db = db
        self.agent = agent

    @overload
    def ask(self, query: str, *, stream: Literal[False] = False, max_results: int = 10) -> tuple[list[ParagraphResult], str]: ...
    @overload
    def ask(self, query: str, *, stream: Literal[True], max_results: int = 10) -> tuple[list[ParagraphResult], Generator[str, None, None]]: ...
    def ask(self, query: str, *, stream: bool = False, max_results: int = 10) -> tuple[list[ParagraphResult], str | Generator[str, None, None]]:
        # semantic search over the database
        results = self.db.query_all_documents(query, max_results=max_results)

        # synthesizer answer from the semantic search results
        answer = synthesize_answer(self.agent, query, [r.paragraph for r in results], stream=stream)

        return results, answer


class ConversationalRagAgent(RagAgent):
    def __init__(self, db: Database, agent: Agent, *, messages: list[Message]|None = None):
        """
        Create a RAG Agent that maintains and refers back to a conversation history

        Args:
            db (Database): the database to query
            agent (Agent): the agent to use for answering questions
            messages (list[Message], optional): the conversation history. Defaults to [].
        """
        self.db = db
        self.agent = agent
        self.messages: list[Message] = messages or []

    @overload
    def ask(self, query: str, *, stream: Literal[False] = False, max_results: int = 10) -> tuple[list[ParagraphResult], str]: ...
    @overload
    def ask(self, query: str, *, stream: Literal[True], max_results: int = 10) -> tuple[list[ParagraphResult], Generator[str, None, None]]: ...
    def ask(self, query: str, *, stream: bool = False, max_results: int = 10) -> tuple[list[ParagraphResult], str | Generator[str, None, None]]:
        if len(self.messages) == 0:
            system_query = f'Please convert the following question to a contextless search query for a database search: "{query}"'
        else:
            system_query = f'Based on any relevant context from the conversation, please convert the following question to a contextless search query for a database search: "{query}"'
        context_free_query = self.agent.multishot_sync(
            [*self.messages, Message(role=Role.system, content=system_query)])
        context_free_query = strip_quotes(context_free_query)

        # semantic search over the database
        results = self.db.query_all_documents(context_free_query, max_results=max_results)

        # synthesizer answer from the semantic search results
        answer = synthesize_answer(
            self.agent,
            query,
            [r.paragraph for r in results],
            stream=stream,
            chat_history=self.messages
        )

        self.messages.append(Message(role=Role.user, content=query))

        # simple case, handle non-streaming answer
        if isinstance(answer, str):
            self.messages.append(Message(role=Role.assistant, content=answer))
            return results, answer

        # generator wrapper so that we can save the answer to the chat history when it is done streaming
        def gen_wrapper():
            res = []
            for token in answer:
                res.append(token)
                yield token

            answer_message = Message(role=Role.assistant, content=''.join(res))
            self.messages.append(answer_message)

        return results, gen_wrapper()


class MultihopRagAgent(RagAgent):
    def __init__(self, db: Database, agent: Agent, *, messages: list[Message]|None = None):
        """
        Create a RAG Agent that can perform multi-hop reasoning (and also maintain + refer back to conversation history)

        Args:
            db (Database): the database to query
            agent (Agent): the agent to use for answering questions
            messages (list[Message], optional): the conversation history. Defaults to [].
        """
        self.db = db
        self.agent = agent
        self.messages: list[Message] = messages or []
        self.query_pattern = re.compile(r'^(\w+)(\(\w+\))?:\s*(.+)$')
        self.selection_pattern = re.compile(r'^\s*\((\d+),\s*(\d+)\)\s*(.*)$')

    @overload
    def ask(self, user_query: str, *, stream: Literal[False] = False, max_query_results: int = 10) -> tuple[list[ParagraphResult], str]: ...
    @overload
    def ask(self, user_query: str, *, stream: Literal[True], max_query_results: int = 10) -> tuple[list[ParagraphResult], Generator[str, None, None]]: ...
    def ask(self, user_query: str, *, stream: bool = False, max_query_results: int = 10) -> tuple[list[ParagraphResult], str | Generator[str, None, None]]:

        # Make the Query context free
        if len(self.messages) == 0:
            system_query = f'If the following query requires context, please add any context to make it a self-contained/context-free query. Otherwise repeat verbatim: "{user_query}"'
        else:
            system_query = f'Based on any relevant context from the conversation, if the following query requires context, please add any context to make it a self-contained/context-free query. Otherwise repeat verbatim: "{user_query}"'
        context_free_query = self.agent.multishot_sync(
            [*self.messages, Message(role=Role.system, content=system_query)])
        context_free_query = strip_quotes(context_free_query)

        # Convert to one or more queries
        raw_queries = self.agent.multishot_sync([
            Message(role=Role.system, content=MULTIQUERY_PROMPT),
            Message(role=Role.user, content=context_free_query),
        ])
        queries: list[Query] = []
        query_strings = [stripped for line in raw_queries.splitlines() if (stripped := line.strip())]
        for query_string in query_strings:
            match = self.query_pattern.match(query_string)
            if match is None:
                raise ValueError(
                    f'Invalid query format: "{query_string}". Must be of the form "name_of_query_target: plain-text query"')
            target, arg, query = match.groups()
            queries.append(Query(target=target, query=query, arg=arg))

        # Run each query
        all_results = []
        for query in queries:
            if query.target == 'query_titles':
                all_results.append(self.db.query_titles(query.query, max_results=max_query_results))
            elif query.target == 'query_authors':
                all_results.append(self.db.query_authors(query.query, max_results=max_query_results))
            elif query.target == 'query_publishers':
                all_results.append(self.db.query_publishers(query.query, max_results=max_query_results))
            elif query.target == 'query_document':
                all_results.append(self.db.query_single_document(query.arg, query.query, max_results=max_query_results))
            elif query.target == 'query_whole_database':
                all_results.append(self.db.query_all_documents(query.query, max_results=max_query_results))
            else:
                raise ValueError(
                    f'Invalid query target: "{query.target}". Must be one of {Query.__annotations__["target"].__args__}')

        # Build prompt for selecting which results are relevant
        results_filter_prompt_chunks = ["Results from queries:"]
        for i, (query, results) in enumerate(zip(queries, all_results)):
            results_filter_prompt_chunks.append(f"({i}) {query}")
            for j, result in enumerate(results):
                results_filter_prompt_chunks.append(f"    ({i}, {j}) {result}")
            results_filter_prompt_chunks.append('')
        results_filter_prompt_chunks.append("Please select which of the previous results are relevant to your queries. Output the tuples (i, j) of the relevant results, one per line. If the result you are selecting was a MetadataResult (i.e. from a title, author, or publisher search), please also come up with a subquery describing what specific information you want from that source. The subquery should immediately follow the selection tuple, separated by a single space. If there are no relevant results, don't output anything. Do not output any other text or comments.")
        results_filter_prompt = '\n'.join(results_filter_prompt_chunks)
        raw_filter_selections = self.agent.multishot_sync([
            Message(role=Role.system, content="You are helping the user search for information in the database. Based on the following query and results from searching the database, please select which results are relevant to the original query."),
            Message(role=Role.user, content=f"Original query: context_free_query"),
            Message(role=Role.assistant, content=f"Refined query(s):\n{raw_queries}"),
            Message(role=Role.system, content=results_filter_prompt),
        ])

        # Collect results specified by agent
        raw_selections = [stripped for line in raw_filter_selections.splitlines() if (stripped := line.strip())]
        selections = []
        for raw_selection in raw_selections:
            match = self.selection_pattern.match(raw_selection)
            if match is None:
                raise ValueError(
                    f'Invalid selection format: "{raw_selection}". Must be of the form "(i, j) optional subquery"')
            i, j, subquery = match.groups()
            selections.append((int(i), int(j), subquery))
        relevant_results: list[tuple[ParagraphResult, None] | tuple[MetadataResult, str]] = []
        for i, j, subquery in selections:
            relevant_results.append((all_results[i][j], subquery))

        # Generate the full list of results
        results: list[ParagraphResult] = []
        for result, subquery in relevant_results:
            if isinstance(result, MetadataResult):
                results.extend(self.db.query_single_document(result.document_id, subquery, max_query_results))
            else:
                results.append(result)

        # Synthesize the answer
        answer = synthesize_answer(
            self.agent, user_query, [r.paragraph for r in results], stream=stream, chat_history=self.messages)

        self.messages.append(Message(role=Role.user, content=user_query))
        if type(answer) == str:
            self.messages.append(Message(role=Role.assistant, content=answer))

            return results, answer

        # generator wrapper so that we can save the answer to the chat history when it is done streaming
        def gen_wrapper():
            res = []
            for token in answer:
                res.append(token)
                yield token

            answer_message = Message(role=Role.assistant, content=''.join(res))
            self.messages.append(answer_message)

        return results, gen_wrapper()


# TODO: include the current date in this prompt
MULTIQUERY_PROMPT = """\
You are a query crafter--you are given a query, and it is your job to craft one or multiple queries that will return the necessary information from the database to answer the original query.

Each query should be a separate line, and be of the following form:
name_of_query_target: query written out in plain text

The following query targets are available:
query_titles: search for documents by title. Returns a list of documents that best match the given title. Only use if you know a specific title that you are looking for.
query_authors: search for documents by author. Returns a list of documents that best match the given author. Only use if you know a specific author that you are looking for.
# query_publishers: tbd, net yet implemented
query_document(doc_id): search for document content from a specific document (requires a valid document ID). returns the best matching paragraphs of the document based on the query.
query_whole_database: search for content in all documents in the database. returns the best matching paragraphs out of all documents based on the query. Usually you should not combine this with other queries.

Here are some concrete examples of splitting up a query:

user's query: Which company among Google, Apple, and Nvidia reported the largest profit margins in their third-quarter reports for 2023?
------should be split into-------
query_titles: Google third-quarter 2023 earnings report
query_titles: Apple third-quarter 2023 earnings report
query_titles: Nvidia third-quarter 2023 earnings report


user's query: How does Apple's sales trend look over the past three years?
------should be split into-------
query_titles: Apple sales report 2021
query_titles: Apple sales report 2022
query_titles: Apple sales report 2023


user's query: What papers has John Smith published?
------should be split into-------
query_authors: John Smith


user's query: What is the impact of climate change on the Amazon rainforest?
------should be split into-------
query_whole_database: climate change impact on the Amazon rainforest


user's query: In document with ID "abc123", what is the author's opinion on the impact of climate change on the Amazon rainforest?
------should be split into-------
query_document(abc123): impact of climate change on the Amazon rainforest

For the following query, please provide the queries that you would like to run on the database (and do not output any other text or comments):
"""
