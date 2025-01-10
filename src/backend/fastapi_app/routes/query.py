from fastapi import APIRouter, Query
from typing import Annotated
import asyncio
from models.query import QueryParams, AdvancedQueryParams, SummarizeParams
from services import *
from services import arxiv
from utilities import log, log_async
from pprint import pprint

router = APIRouter()


@router.get("")
async def query(params: Annotated[QueryParams, Query()]) -> dict:
    """
    Executes a basic query that searches keywords across all query fields

    Args:
        all (str, required): keyword to search across all fields
        boolean_operator (str, optional): logical operator ('AND', 'OR', 'ANDNOT'; default: 'AND')
        start (int, optional): start index for pagination (default: 0)
        max_results (int, optional): maximum number of results (default: 5)
        sort_by (str, optional): sort criteria ('relevance', 'lastUpdatedDate', 'submittedDate')
        sort_order (str, optional): sort order ('ascending', 'descending')

    Returns:
        dict: a dictionary containing arXiv data
    """
    # Fetch data from arXiv API
    async with log_async("Fetching data from arXiv API"):
        arxiv_params = params.to_arxiv()
        arxiv_response = await arxiv.fetch(**arxiv_params)

    # pprint(arxiv_response)
    # Extract entries and respective PDF links
    entries = []
    if "entry" in arxiv_response["feed"]:
        entries = arxiv_response["feed"]["entry"]
    if not isinstance(entries, list):
        entries = [entries]

    pdf_links = [
        link["@href"]
        for entry in entries
        for link in entry["link"]
        if link.get("@type") == "application/pdf"
    ]
    # Build final output
    arxiv_data = [
        {
            "id": entry["id"],
            "updated": entry["updated"],
            "published": entry["published"],
            "title": entry["title"],
            "abstract": entry["summary"],
            "author": entry["author"],
            "pdf": pdf_link,
        }
        for entry, pdf_link in zip(entries, pdf_links)
    ]
    totalResults = arxiv_response["feed"]["opensearch:totalResults"]["#text"]
    print(totalResults, flush=True)

    return {"arxiv": arxiv_data, "totalResults": totalResults}


@router.get("/advanced")
async def query_advanced(params: Annotated[AdvancedQueryParams, Query()]) -> dict:
    """
    Executes an advanced query that searches keywords across specific query fields
    If multiple fields are provided, they are combined using the same boolean_operator

    Args:
        title, author, abstract, comment, journal_reference, subject_category,
        report_number, id_list (at least one required): keyword to search in a specific field
        boolean_operator (str, optional): logical operator ('AND', 'OR', 'ANDNOT'; default: 'AND')
        start (int, optional): start index for pagination (default: 0)
        max_results (int, optional): maximum number of results (default: 5)
        sort_by (str, optional): sort criteria ('relevance', 'lastUpdatedDate', 'submittedDate')
        sort_order (str, optional): sort order ('ascending', 'descending')

    Returns:
        dict: a dictionary containing arXiv data
    """
    # Fetch data from arXiv API
    async with log_async("Fetching data from arXiv API"):
        arxiv_params = params.to_arxiv()
        arxiv_response = await arxiv.fetch(**arxiv_params)

    # Extract entries and respective PDF links
    entries = []
    if "entry" in arxiv_response["feed"]:
        entries = arxiv_response["feed"]["entry"]
    if not isinstance(entries, list):
        entries = [entries]

    pdf_links = [
        link["@href"]
        for entry in entries
        for link in entry["link"]
        if link.get("@type") == "application/pdf"
    ]

    # Build final output
    arxiv_data = [
        {
            "id": entry["id"],
            "updated": entry["updated"],
            "published": entry["published"],
            "title": entry["title"],
            "abstract": entry["summary"],
            "author": entry["author"],
            "pdf": pdf_link,
        }
        for entry, pdf_link in zip(entries, pdf_links)
    ]
    totalResults = arxiv_response["feed"]["opensearch:totalResults"]["#text"]

    return {"arxiv": arxiv_data, "totalResults": totalResults}


@router.get("/summarize")
async def summarize(params: Annotated[SummarizeParams, Query()]) -> dict:
    pdf_link = params.get_pdf_link()

    rd = RedisSingleton()
    status: ProcessStatus = await rd.get_pdf_process_status(pdf_link)

    if status is not None:
        delay = 1
        while status != ProcessStatus.COMPLETED and delay <= 240:
            await asyncio.sleep(delay)
            status = await rd.get_pdf_process_status(pdf_link)
            delay *= 2
        if status == ProcessStatus.COMPLETED:
            await rd.store_pdf_process_status(pdf_link, ProcessStatus.COMPLETED)
            return {"summary": await rd.get_pdf_summary(pdf_link)}

    try:
        await rd.store_pdf_process_status(pdf_link, ProcessStatus.PROCCESSING)
        async with log_async("Fetching PDF from arXiv"):
            pdf_bytes = await fetch_single_pdf(pdf_link)

        with log("Chunking PDF into sections"):
            chunked_pdf = ChunkerSingleton().chunk_pdf(pdf_bytes)

        with log("Summarizing each chunk"):
            chunked_pdf_rdd = (
                SparkSessionSingleton().get_spark_context().parallelize(chunked_pdf)
            )
            summary = (
                SummarizerSingleton()
                .summarize_chunked_sections(chunked_pdf_rdd)
                .collect()
            )

        await rd.store_pdf_process_status(pdf_link, ProcessStatus.COMPLETED)
        await rd.store_pdf_summary(pdf_link, summary)
        return {"summary": summary}
    except Exception as e:
        status = await rd.get_pdf_process_status(pdf_link)
        if not status or status != ProcessStatus.COMPLETED:
            await rd.store_pdf_process_status(pdf_link, ProcessStatus.FAILED)
        return {"summary": "Error", "error": str(e)}
