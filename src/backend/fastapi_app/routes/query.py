from fastapi import APIRouter, Query
from typing import Annotated
import asyncio, uuid
from models.query import QueryParams, AdvancedQueryParams
from services import arxiv, pdf

router = APIRouter()

@router.get('')
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
    arxiv_params = params.to_arxiv()
    arxiv_data = await arxiv.fetch(**arxiv_params)

    pdfs = [
        link['@href']
        for entry in arxiv_data['feed']['entry']
        for link in entry['link']
        if link.get('@type') == 'application/pdf'
    ]
    print(pdfs)
    request_id = str(uuid.uuid4())
    await pdf.store_in_redis(request_id, pdfs)

    return {'arxiv': arxiv_data}

@router.get('/advanced')
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
    # # Make concurrent calls
    # arxiv_data, elsevier_data, ieee_data = await asyncio.gather(arxiv.fetch(), elsevier.fetch(), ieee.fetch())

    arxiv_params = params.to_arxiv()
    arxiv_data = await arxiv.fetch(**arxiv_params)
    
    return {'arxiv': arxiv_data}
