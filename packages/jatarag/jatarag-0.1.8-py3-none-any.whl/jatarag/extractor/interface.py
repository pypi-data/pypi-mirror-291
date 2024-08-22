from __future__ import annotations

from typing import IO, Any
from abc import ABC, abstractmethod
from pathlib import Path


class Extractor(ABC):
    """abstract class for extracting text from a pdf file and splitting into paragraphs"""
    @abstractmethod
    def extract_pdf_text(self, path: Path, log: IO[Any] | int | None = None) -> str: ...

    @abstractmethod
    def convert_to_paragraphs(self, text: str) -> list[str]: ...
