from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, replace
from collections import defaultdict


@dataclass
class Result(ABC):
    score: float  # should be a value from 0 to 1

    @abstractmethod
    def get_id(self) -> str:
        """return a unique identifier for the content this result corresponds to"""

    def __post_init__(self):
        if self.score < 0 or self.score > 1:
            raise ValueError(f"score must be between 0 and 1, got {self.score}")


@dataclass
class Paragraph:
    document_id: str
    paragraph_idx: int
    paragraph: str


@dataclass
class Metadata:
    document_id: str
    title: str
    author: str
    publisher: str


@dataclass
class ParagraphResult(Result, Paragraph):
    def get_id(self) -> str:
        return f'{self.document_id}-{self.paragraph_idx}'


@dataclass
class MetadataResult(Result, Metadata):
    def get_id(self) -> str:
        return self.document_id


class Database(ABC):
    # TODO: long-term, would love to be able to omit some methods (e.g. if metadata wasn't available), and dynamically update the llm prompt to not mention them

    @abstractmethod
    def query_all_documents(self, query: str, max_results: int = 10) -> list[ParagraphResult]:
        """perform a search over all document paragraphs in the database for the given query"""

    @abstractmethod
    def query_single_document(self, document_id: str, query: str, max_results: int = 10) -> list[ParagraphResult]:
        """perform a search over a single document in the database for the given query"""

    @abstractmethod
    def query_titles(self, query: str, max_results: int = 10) -> list[MetadataResult]:
        """perform a search over all document titles in the database for the given query"""

    @abstractmethod
    def query_authors(self, author: str, max_results: int = 10) -> list[MetadataResult]:
        """perform a search over all document authors in the database for the given query"""

    @abstractmethod
    def query_publishers(self, publisher: str, max_results: int = 10) -> list[MetadataResult]:
        """perform a search over all document publishers in the database for the given query"""


def reciprocal_rank_fusion(results: list[list[Result]], k: float = 60) -> list[Result]:
    """
    Combines multiple lists of results using a modified version of the Reciprocal Rank Fusion method

    This can be used in concrete implementations of the Database interface to allow more advanced search strategies by
    combining multiple search methods. For example, you could combine a semantic search + keyword search over document
    paragraphs, or phonetic search + fuzzy search over author names.

    Parameters:
        results (list[list[Result]]): a list of result lists to be fused together. Each result list need not be sorted
        k (float): a constant to control the importance of the rank vs frequency of the result appearing in multiple 
            lists. Higher values of k will reduce the impact of the rank differences, making the total number of times a
            document appears in the results lists more significant. Conversely, lower values of k will give more
            importance to the ranks of the document in the individual lists

    Returns:
        list[Result]: a fused list of results. Scores will be updated both based on the fused rankings
    """

    # ensure results are sorted by score
    results = [sorted(result_list, key=lambda x: x.score, reverse=True) for result_list in results]

    # determine the maximum possible score for normalization
    max_possible_score = len(results) / (1+k)

    # build map from each result_id to all its rankings
    ranks_map: dict[str, list[int]] = defaultdict(list)     # {result_id: [rank1, rank2, ...]}
    result_map: dict[str, Result] = {}                      # {result_id: Result}
    for result_list in results:
        for i, result in enumerate(result_list):
            result_id = result.get_id()
            result_map[result_id] = result  # might overwrite a previous one, but we just need one of them
            ranks_map[result_id].append(i+1)

    # Compute the fused scores based on rrf of the ranks
    scores = [(result_id, sum(1/(rank+k) for rank in ranks)) for result_id, ranks in ranks_map.items()]
    scores.sort(key=lambda x: x[1], reverse=True)

    # generate the fused list of results, and update the scores (normalize based on the maximum possible score)
    fused_results = [replace(result_map[result_id], score=score/max_possible_score) for result_id, score in scores]

    return fused_results
