from abc import ABC, abstractmethod


class TextVectorizer(ABC):

    @abstractmethod
    async def __call__(self, q: list[str]) -> list[list[float]]:
        return []
