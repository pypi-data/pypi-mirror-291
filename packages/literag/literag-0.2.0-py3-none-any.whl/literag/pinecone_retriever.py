import asyncio
import httpx
from typing import Any

from literag.text_vectorizer import TextVectorizer
from literag.retrieval_service import Document, RetrievalService


class PineconeRetriever(RetrievalService):
    """
    See: https://docs.pinecone.io/reference/api/data-plane/query for more information on the Pinecone VDB query API.

    Attributes:
        index_name (str): name of the Pinecone index to query.
        api_key (str): Pinecone API key.
        text_vectorizer (TextVectorizer): object to convert string queries to embeddings.
        index_host (str): host of the Pinecone index to query.
    """

    def __init__(
        self,
        index_name: str,
        api_key: str,
        text_vectorizer: TextVectorizer,
        index_host: str | None = None,
    ):
        """
        Args:
            index_name (str): name of the Pinecone index to query.
            api_key (str): Pinecone API key.
            text_vectorizer (TextVectorizer): object to convert string queries to embeddings.
            index_host (str | None, optional): host of the Pinecone index to query. If None it will be retrieved from the Pinecone API. Defaults to None.
        """
        self.index_name = index_name
        self.api_key = api_key
        self.text_vectorizer = text_vectorizer
        self.index_host = index_host or self._get_index_host()

    def _get_index_host(self) -> str:
        """Retrieves the host of the Pinecone index from the Pinecone API."""
        with httpx.Client() as client:
            response = client.get(
                f"https://api.pinecone.io/indexes/{self.index_name}",
                headers={"Api-Key": self.api_key},
            )
            response.raise_for_status()
            json_resp = response.json()
        return json_resp["host"]

    async def __call__(
        self,
        queries: list[str],
        top_k: int,
        filters: dict | None = None,
        pool_limit: int = 100,
    ):
        """
        Retrieves the top k documents based on the text queries.

        Args:
            queries (list[str]): list of queries to retrieve.
            top_k (int): number of results to return.
            filters (dict | None, optional): filter dictionary to pass to the Pinecone query API. Defaults to None.
            pool_limit (int, optional): max number of concurrent requests to make. Defaults to 100.
        """
        return await self._retrieve_vectorizing(
            queries, top_k, filters=filters, pool_limit=pool_limit
        )

    async def query_request(self, vect: list[float], pool_limit: int = 100, **kw_req):
        """Sends a query request to the Pinecone API."""
        async with asyncio.Semaphore(pool_limit), httpx.AsyncClient() as client:
            return await client.post(
                f"https://{self.index_host}/query",
                headers={"Api-Key": self.api_key, "Content-Type": "application/json"},
                json={"vector": vect, **kw_req},
            )

    async def retrieve(
        self,
        vectors: list[list[float]],
        top_k: int,
        filters: dict | None = None,
        pool_limit: int = 100,
        **kwargs,
    ) -> list[list[Document]]:
        """
        Retrieves the top k documents based on the list of vector embeddings.

        Args:
            vectors (list[list[float]]): list of vectors to search for.

        Returns:
            list[Document]: list of documents.
        """
        requests_kw: dict = dict(
            top_k=top_k, filter=filters, include_values=True, include_metadata=True, **kwargs
        )
        requests_kw = {k: v for k, v in requests_kw.items() if v is not None}
        async with asyncio.TaskGroup() as tg:  # retrieve with httpx requests concurrently
            async_tasks = [
                tg.create_task(self.query_request(v, pool_limit, **requests_kw)) for v in vectors
            ]
        responses = [task.result() for task in async_tasks]
        results: list[dict[str, Any]] = [
            (resp.json() if resp.status_code == 200 else {"error": resp.text, "matches": []})
            for resp in responses
        ]

        documents = [  # results parsed into Document objects
            [
                Document(
                    Id=doc["id"],
                    text=doc["metadata"].pop("text"),
                    embedding=doc["values"],
                    metadata=doc["metadata"],
                )
                for doc in results_query["matches"]
            ]
            for results_query in results
        ]

        # documents = [  # results parsed into Document objects
        #     [
        #         Document(
        #             Id=doc["id"],
        #             text=doc["metadata"]["text"],
        #             embedding=doc["values"],
        #             standard=doc["metadata"].get("standard", ""),
        #             num_page=int(doc["metadata"].get("page", 0)),
        #             figure_index=(
        #                 f_ind if (f_ind := int(doc["metadata"].get("figure", -1))) >= 0 else None
        #             ),
        #         )
        #         for doc in results_query["matches"]
        #     ]
        #     for results_query in results
        # ]

        return documents
