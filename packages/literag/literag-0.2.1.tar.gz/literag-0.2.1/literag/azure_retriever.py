# from azure.search.documents.aio import SearchClient
# from azure.search.documents.models import QueryType, VectorQuery
# from openai import AsyncAzureOpenAI

# from literag.retrieval_service import Document, RetrievalService


# class AzureRetriever(RetrievalService):
#     pass
#     """Retrieves documents from an Azure AI Search index"""

#     def __init__(
#         self,
#         search_client: SearchClient,
#         openai_client: AsyncAzureOpenAI,
#         embedding_deployment: str | None,  # Not needed for retrieval_mode="text"
#         embedding_model: str = "text-embedding-ada-002",
#         embedding_dimensions: int = 1536,
#     ):
#         self.search_client = search_client
#         self.openai_client = openai_client
#         self.embedding_deployment = embedding_deployment
#         self.embedding_model = embedding_model
#         self.embedding_dimensions = embedding_dimensions

#     async def __call__(
#         self,
#         top: int,
#         query_text: str | None,
#         filter_key: str | None,
#         vectors: list[VectorQuery],
#         use_semantic_ranker: bool,
#         use_semantic_captions: bool,
#         min_search_score: float | None,
#         min_reranker_score: float | None,
#     ) -> list[Document]:
#         search_text = query_text or ""
#         search_vectors = vectors or []
#         if use_semantic_ranker:
#             results = await self.search_client.search(
#                 search_text=search_text,
#                 filter=filter_key,
#                 top=top,
#                 query_caption="extractive|highlight-false" if use_semantic_captions else None,
#                 vector_queries=search_vectors,
#                 query_type=QueryType.SEMANTIC,
#                 semantic_configuration_name="default",
#                 semantic_query=query_text,
#             )
#         else:
#             results = await self.search_client.search(
#                 search_text=search_text,
#                 filter=filter_key,
#                 top=top,
#                 vector_queries=search_vectors,
#             )

#         documents = []
#         async for page in results.by_page():
#             async for document in page:
#                 documents.append(
#                     Document(
#                         key_id=document["id"],
#                         content=document["content"],
#                         embedding=document["embedding"],
#                         standard=document["standard"],
#                         sourcepage=document.get("sourcepage"),
#                         sourcefile=document.get("sourcefile"),
#                         score=document.get("score"),
#                         reranker_score=document.get("reranker_score"),
#                     )
#                 )

#             qualified_documents = [
#                 doc
#                 for doc in documents
#                 if (
#                     (doc.score or 0) >= (min_search_score or 0)
#                     and (doc.reranker_score or 0) >= (min_reranker_score or 0)
#                 )
#             ]

#         return qualified_documents
