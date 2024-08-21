from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from typing import Any

from literag.text_vectorizer import TextVectorizer


@dataclass
class Document:
    Id: str
    text: str
    embedding: list[float]
    metadata: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def trim_text(cls, text: str):
        """Returns a trimmed string from the content."""
        return f"{text[:100]} ..." if len(text) > 200 else text

    @classmethod
    def trim_embedding(cls, embedding: list[float]):
        """Returns a trimmed list of floats from the vector embedding."""
        if embedding:
            if len(embedding) > 2:
                # Format the embedding list to show the first 2 items followed by the count of the remaining items."""
                return f"[{embedding[0]}, {embedding[1]} ... + {len(embedding) - 2} more]"
            else:
                return str(embedding)
        return None

    def __repr__(self) -> str:
        """returns a string representation of the document with the embedding trimmed."""
        return f"{self.Id}: \nText: {Document.trim_text(self.text)}\nEmbedding: {Document.trim_embedding(self.embedding)}"


class RetrievalService(ABC):

    def __init__(self, text_vectorizer: TextVectorizer, **kwargs):
        self.text_vectorizer = text_vectorizer

    @abstractmethod
    async def __call__(self, queries: list[str], top_k: int, **kwargs) -> list[Document]:
        pass

    async def _retrieve_vectorizing(
        self, queries: list[str], top_k: int, **kwargs
    ) -> list[list[Document]]:
        return await self.retrieve(await self.text_vectorizer(queries), top_k, **kwargs)

    @abstractmethod
    async def retrieve(self, vectors: list[list[float]], top_k, **kwargs) -> list[list[Document]]:
        pass
