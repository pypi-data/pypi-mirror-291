from typing import Protocol
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Result(ABC):
    score: float  # should be a value from 0 to 1

    @abstractmethod
    def get_id(self) -> str:
        """return a unique identifier for the content this result corresponds to"""

    def __post_init__(self):
        if self.score < 0 or self.score > 1:
            raise ValueError(f"score must be between 0 and 1, got {self.score}")


class QueryMethod(Protocol):
    def __call__(self, query: str, max_results: int = 10) -> list[Result]: ...


def query_decorator(method: QueryMethod) -> QueryMethod:
    # people would call this when defining concrete subclasses to add extra query methods that the agent can see
    ...


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

    # TBD perhaps a decorator here to make this work correctly
    # also what about allowing for adding extra methods that the agent could use for extra types of queries it could make
    @property
    def query_authors(self) -> QueryMethod | None: ...

    # this would probably be defined in the concrete subclass
    # @abstractmethod
    # def query_authors(self, author: str, max_results: int = 10) -> list[MetadataResult]:
    #     """perform a search over all document authors in the database for the given query"""

    # this would probably be defined in the concrete subclass
    # @abstractmethod
    # def query_publishers(self, publisher: str, max_results: int = 10) -> list[MetadataResult]:
    #     """perform a search over all document publishers in the database for the given query"""


class ConcreteDatabase(Database):
    ...
