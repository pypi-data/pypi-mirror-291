import asyncio
from contextlib import contextmanager
import json
from pathlib import Path
from typing import Annotated, Optional

from openai import AsyncAzureOpenAI
from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn  # , track
import typer

from literag.openai_vectorizer import OpenAIEmbModel, OpenAIVectorizer
from literag.pinecone_retriever import PineconeRetriever
from literag.retrieval_service import Document

app = typer.Typer(no_args_is_help=True, rich_markup_mode="markdown")


def file_type_callback(value: Path | None, file_type: str):
    if value and value.suffix != f".{file_type}":
        raise typer.BadParameter(f"Only {file_type.upper()} files are supported")
    return value


@contextmanager
def rich_progress(description: str):
    with Progress(
        SpinnerColumn(), TextColumn("[progress.description]{task.description}"), transient=True
    ) as progress:
        progress.add_task(description=description, total=None)
        yield progress


@app.callback()
def callback():
    """
    Retrieve documents from Retrieval Services.
    """
    pass


def parse_dict(value: str) -> dict:
    return json.loads(value)


def display_documents(queries: list[str], documents: list[list[Document]]):
    for query, docs in zip(queries, documents):
        print(f"\nQuery: {query}")
        for i, doc in enumerate(docs):
            print(f"Document nº {i+1}:\n{doc}")


@app.command(
    "query-pc",
    epilog="""Example: literag query-pc 'test query' 'random words' 5 --filters '{"figure": {"$lte": -1}}' --verbose""",
)
def retrieve_from_pinecone(
    queries: Annotated[
        list[str],
        typer.Argument(
            help="List of queries to retrieve",
            show_default=False,
        ),
    ],
    top_k: Annotated[
        int,
        typer.Argument(
            help="Number of results to retrieve",
            show_default=False,
        ),
    ],
    index: Annotated[
        str,
        typer.Option(
            help="Name of the index where content should be indexed",
            rich_help_panel="Pinecone",
            envvar="PINECONE_INDEX",
            prompt=True,
            show_default=False,
        ),
    ],
    api_key: Annotated[
        str,
        typer.Option(
            help="Pinecone API key",
            rich_help_panel="Pinecone",
            envvar="PINECONE_KEY",
            prompt=True,
            show_default=False,
        ),
    ],
    openai_service: Annotated[
        str,
        typer.Option(
            help="Name of the Azure OpenAI service used for the embeddings",
            rich_help_panel="OpenAI",
            envvar="OPENAI_SERVICE",
            prompt=True,
            show_default=False,
        ),
    ],
    emb_deployment: Annotated[
        str,
        typer.Option(
            help="Name of the deployment and of the (Azure) OpenAI for an embedding model",
            rich_help_panel="OpenAI",
            envvar="OPENAI_EMB_DEPLOYMENT",
            prompt=True,
            show_default=False,
        ),
    ],
    openai_key: Annotated[
        str,
        typer.Option(
            help="Use this Azure OpenAI account key instead of the current user identity to login",
            rich_help_panel="OpenAI",
            envvar="OPENAI_KEY",
            prompt=True,
            show_default=False,
        ),
    ],
    index_host: Annotated[
        Optional[str],
        typer.Option(
            help="Pinecone Index Host",
            rich_help_panel="Pinecone",
            envvar="PINECONE_INDEX_HOST",
            show_default=False,
        ),
    ] = None,
    emb_model: Annotated[
        OpenAIEmbModel,
        typer.Option(
            help="Name of the model and of the (Azure) OpenAI model for an embedding model",
            rich_help_panel="OpenAI",
            envvar="OPENAI_EMB_MODEL_NAME",
            prompt=True,
            show_default=False,
        ),
    ] = OpenAIEmbModel.ada,
    filters: Annotated[
        Optional[dict],
        typer.Option(
            rich_help_panel="Control",
            help="Filters to apply to the query",
            show_default=False,
            parser=parse_dict,
        ),
    ] = None,
    pool_limit: Annotated[
        int,
        typer.Option(
            rich_help_panel="Control",
            help="Max number of concurrent requests to send to the Pinecone API",
            show_default=False,
        ),
    ] = 100,
    verbose: Annotated[
        bool,
        typer.Option(
            help="Prints the retrieved documents",
            show_default=False,
        ),
    ] = False,
):
    openai_client = AsyncAzureOpenAI(
        azure_endpoint=f"https://{openai_service}.openai.azure.com",
        api_version="2024-02-15-preview",
        api_key=openai_key,
    )
    text_vectorizer = OpenAIVectorizer(
        openai_client=openai_client,
        embedding_model=emb_model,
        embedding_deployment=emb_deployment,
    )
    pc_retriever = PineconeRetriever(
        index_name=index, api_key=api_key, text_vectorizer=text_vectorizer, index_host=index_host
    )
    with rich_progress("Retrieving documents"):
        documents = asyncio.run(
            pc_retriever(queries, top_k, filters=filters, pool_limit=pool_limit)
        )
    if verbose:
        display_documents(queries, documents)
    return documents


@app.command()
@app.command(
    name="azure",
    epilog=r"Example: literag azure '",
)
def azure_retrieval(
    queries: Annotated[
        list[str],
        typer.Argument(
            help="List of queries to retrieve",
            show_default=False,
        ),
    ],
    top_k: Annotated[
        int,
        typer.Argument(
            help="Number of results to retrieve",
            show_default=False,
        ),
    ],
    search_service: Annotated[
        str,
        typer.Option(
            help="Name of the Azure AI Search service where content should be indexed",
            rich_help_panel="Azure Search",
            envvar="AZ_SEARCH_SERVICE",
            prompt=True,
            show_default=False,
        ),
    ],
    index: Annotated[
        str,
        typer.Option(
            help="Name of the index where content should be indexed",
            rich_help_panel="Azure Search",
            envvar="AZ_INDEX",
            prompt=True,
            show_default=False,
        ),
    ],
    search_key: Annotated[
        str,
        typer.Option(
            help="Use this Azure AI Search account key instead of the current user identity to login",
            rich_help_panel="Azure Search",
            envvar="AZ_SEARCH_KEY",
        ),
    ],
    openai_service: Annotated[
        str,
        typer.Option(
            help="Name of the Azure OpenAI service used for the embeddings",
            rich_help_panel="OpenAI",
            envvar="OPENAI_SERVICE",
            prompt=True,
            show_default=False,
        ),
    ],
    emb_deployment: Annotated[
        str,
        typer.Option(
            help="Name of the deployment and of the (Azure) OpenAI for an embedding model",
            rich_help_panel="OpenAI",
            envvar="OPENAI_EMB_DEPLOYMENT",
            prompt=True,
            show_default=False,
        ),
    ],
    openai_key: Annotated[
        str,
        typer.Option(
            help="Use this Azure OpenAI account key instead of the current user identity to login",
            rich_help_panel="OpenAI",
            envvar="OPENAI_KEY",
        ),
    ],
    emb_model: Annotated[
        OpenAIEmbModel,
        typer.Option(
            help="Name of the model and of the (Azure) OpenAI model for an embedding model",
            rich_help_panel="OpenAI",
            envvar="OPENAI_EMB_MODEL_NAME",
            prompt=True,
            show_default=False,
        ),
    ] = OpenAIEmbModel.ada,
):
    pass

    # queries: Annotated[
    #     Path,
    #     typer.Argument(
    #         help="Path to the analysis JSON to be ingested",
    #         exists=True,
    #         dir_okay=False,
    #         resolve_path=True,
    #         show_default=False,
    #         callback=lambda x: file_type_callback(x, "json"),
    #     ),
    # ],
