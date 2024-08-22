from __future__ import annotations

from abc import ABC, abstractmethod
import numpy as np


class Embedder(ABC):
    """abstract class for embedding a list of paragraphs into a matrix"""
    @abstractmethod
    def embed_paragraphs(self, paragraphs: list[str]) -> np.ndarray: ...
