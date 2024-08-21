from enum import auto, StrEnum
from dataclasses import dataclass
from typing import TypedDict

from openai import AsyncOpenAI

from literag.text_vectorizer import TextVectorizer


@dataclass(frozen=True, kw_only=True, slots=True)
class OpenAIEmbModelData:
    """Dataclass for a text embedding models"""

    name: str
    default_dim: int  # Will be used if the user does not specify the dimensions
    support_custom_dim: bool  # Whether the model supports to configure the dimensions


OPENAI_EMB_MODELS = {
    "ada": OpenAIEmbModelData(
        name="text-embedding-ada-002", default_dim=1536, support_custom_dim=False
    ),
    "small3": OpenAIEmbModelData(
        name="text-embedding-3-small", default_dim=1536, support_custom_dim=True
    ),
    "large3": OpenAIEmbModelData(
        name="text-embedding-3-large", default_dim=3072, support_custom_dim=False
    ),
}


class OpenAIEmbModel(StrEnum):
    ada = auto()
    small3 = auto()
    large3 = auto()


class OpenAIVectorizer(TextVectorizer):
    """Converts a string query to a vector embedding using the OpenAI API standard."""

    def __init__(
        self,
        openai_client: AsyncOpenAI,
        embedding_model: OpenAIEmbModel = OpenAIEmbModel.ada,
        embedding_deployment: str | None = None,
        embedding_dimensions: int | None = None,
    ):
        """Initializes the OpenAIVectorizer.

        Args:
            openai_client: OpenAI API client.
            embedding_model: OpenAI model to use for the embedding. Defaults to OpenAIEmbModel.ada.
            embedding_deployment: Deployment of the model to use. If None, the name the model will be used. Defaults to None.
            embedding_dimensions: Number of dimensions for the embedding. If None, the default dimensions of the model will be used. Defaults to None.
        """
        self.openai_client = openai_client
        self.embedding_model_data = OPENAI_EMB_MODELS[embedding_model]
        self.embedding_deployment = embedding_deployment or self.embedding_model_data.name
        self.embedding_dimensions = embedding_dimensions or self.embedding_model_data.default_dim

    async def __call__(self, q: list[str]):
        class ExtraArgs(TypedDict, total=False):
            dimensions: int

        dimensions_args: ExtraArgs = (
            {"dimensions": self.embedding_dimensions}
            if self.embedding_model_data.support_custom_dim
            else {}
        )

        embedding_response = await self.openai_client.embeddings.create(
            input=q, model=self.embedding_deployment, **dimensions_args
        )
        return [emb.embedding for emb in embedding_response.data]
