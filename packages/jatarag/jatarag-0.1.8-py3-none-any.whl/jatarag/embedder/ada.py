from __future__ import annotations

import numpy as np
import tiktoken
from openai import OpenAI
from typing import Literal

from .interface import Embedder
from jatarag.utils import OpenAIUtils


client = OpenAI()


def get_embeddings(texts: list[str], model: Literal["text-embedding-ada-002", "text-embedding-3-small", "text-embedding-3-large"]):
    res = client.embeddings.create(input=texts, model=model)
    embeddings = [r.embedding for r in res.data]
    return embeddings


class AdaEmbedder(Embedder, OpenAIUtils):
    def __init__(self):
        self.max_tokens = 8192
        self.num_feature = 1536
        self.tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002")

    def embed_paragraphs(self, paragraphs: list[str]) -> np.ndarray:
        """embed a list of paragraphs into a list of vectors. Output size is (num_paragraphs, num_features)"""

        # before embedding, truncate any paragraphs that are too many tokens
        truncated_paragraphs = [self.tokenizer.decode(self.tokenizer.encode(p)[:self.max_tokens]) for p in paragraphs]

        if len(truncated_paragraphs) == 0:
            paragraph_embeddings = np.zeros((0, self.num_feature))
        else:
            paragraph_embeddings = np.array(get_embeddings(truncated_paragraphs, model="text-embedding-ada-002"))

        return paragraph_embeddings
