# Jatarag

A straightforward library for integrating Retrieval Augmented Generation (RAG) capabilities. RAG is an approach for mitigating LLM hallucinations by grounding the generation process to information retrieved from a corpus of documents. The basic sequence is like so:

1. Documents in the corpus are split into chunks, typically paragraphs, and each chunk is embedded with an LLM into a single vector
2. A query is posed to the RAG agent
3. The query is embedded using the same LLM as the documents
4. The embedded query is used to search the corpus via the cosine similarity to the embedded chunks
5. The top N chunks are retrieved, and their text, combined with the original query, is fed into the LLM to generate an answer

Currently this library provides 3 types of RAG agents:

- `SimpleRagAgent`: a no-frills RAG agent that can answer single questions. Each question is treated as independent, and no chat history is maintained.
- `ConversationalRagAgent`: a RAG agent that can answer multiple questions in a conversational context. The agent maintains a chat history, and can use previous questions and answers to inform future answers.
- `MultihopRagAgent`: a RAG agent implementing Multi-hop reasoning, meaning it can break the query down into multiple sub-queries if necessary to find suitable information from within the corpus of documents.

> The simpler agents are more responsive, whereas the complex ones (especially `MultihopRagAgent`) can take longer to begin responding as they require more steps before they can generate an answer. Once the answer is being generated, they should all take about the same speed (assuming the same LLM is being used).

## Installation

Jatarag is available on pypi, and can be installed via pip:

```bash
pip install jatarag
```

## Development

```bash
git clone git@github.com:jataware/jatarag.git
cd jatarag
pip install poetry
poetry install
```

## Usage

Setting up a simple RAG agent is pretty simple, you just need to provide compatible instances of `Database` and `Agent`:

```python
from jatarag.agent import Agent
from jatarag.db import Database
from jatarag.librarian import SimpleRagAgent

db: Database = SomeDatabaseImplementation()
agent: Agent = SomeAgentImplementation()

librarian = SimpleRagAgent(db, agent)

answer = librarian.ask('What effects do locust swarms have on agriculture in East Africa?')
```

`Database` is the interface to your corpus of documents, and `Agent` is the interface to your LLM. Any of the RAG Agent implementations will take these two objects and provide a method `ask` for querying the corpus and generating an answer. You may provide your own implementations, or use the built-in ones, or any combination thereof.

### Implementing new DB

```python
from jatarag.db import Database, ParagraphResult, MetadataResult, reciprocal_rank_fusion

# implementation of the database interface
class MyDB(Database):
    def __init__(self, ...): ...

    # required interface methods
    def query_all_documents(self, query: str, max_results: int = 10) -> list[ParagraphResult]: ...

    def query_single_document(self, document_id: str, query: str, max_results: int = 10) -> list[ParagraphResult]: ...

    def query_titles(self, query: str, max_results: int = 10) -> list[MetadataResult]: ...

    def query_authors(self, author: str, max_results: int = 10) -> list[MetadataResult]: ...

    def query_publishers(self, publisher: str, max_results: int = 10) -> list[MetadataResult]: ...

    # any other methods you need
    # ...


```

> Note: `reciprocal_rank_fusion` is provided to allow for building more complex searches out of simpler ones. For example, when querying titles, it might make sense to do both a semantic query and a keyword query, and then combine the results. For querying authors, an optimal combination might be to combine a fuzzy search with a phonetic search. `reciprocal_rank_fusion` can combine multiple sets of search results into a master list, while logically computing the new ranks of each result.

### Using built-in implementations

If you'd like, you can use the built-in `FileSystemDB` which manages a directory of documents directly on the filesystem, which might be useful for local testing. You will either need to provide implementations for document extraction, and document embedding, or use the built-in `NougatExtractor` and `AdaEmbedder` classes respectively. See [jatarag/demo.py](jatarag/demo.py) for a more complete example:

```python
from jatarag.db import FileSystemDB
from jatarag.extractor import NougatExtractor
from jatarag.embedder import AdaEmbedder
from jatarag.agent import OpenAIAgent
from jatarag.librarian import MultihopRagAgent

# built-in database (including extractor and embedder)
extractor = NougatExtractor(batch_size=batch_size)
embedder = AdaEmbedder()
db = FileSystemDB(path, extractor=extractor, embedder=embedder)

# built-in agent
agent = OpenAIAgent(model='gpt-4o')

# Rag agent just needs a database and an agent
librarian = MultihopRagAgent(db, agent)

# ask a question based on the corpus
answer = librarian.ask('How has climate change affected crop yields in sub-Saharan Africa?')
```

> You may provide your own implementations of the `Extractor`, `Embedder` and `Agent` classes, as long as they conform to the expected interfaces defined in [jatarag/extractor/interface.py](jatarag/extractor/interface.py), [jatarag/embedder/interface.py](jatarag/embedder/interface.py), and [jatarag/agent.py](jatarag/agent.py) respectively. This allows you to plug in your own models for extracting documents, embedding document chunks, and generating answers.
