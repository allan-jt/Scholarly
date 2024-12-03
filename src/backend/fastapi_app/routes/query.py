from fastapi import APIRouter, HTTPException
import asyncio
from routes.arxiv import fetch_arxiv

router = APIRouter()

@router.get('/')
async def query(all: str):
    data = await query_advanced(all=all)

    return data

@router.get('/advanced')
async def query_advanced(
    title: str | None = None,
    author: str | None = None,
    abstract: str | None = None,
    comment: str | None = None,
    journal_reference: str | None = None,
    subject_category: str | None = None,
    report_number: str | None = None,
    all: str | None = None,
    id_list: str | None = None,
    boolean_operator: str | None = 'AND',
    start: int | None = 0,
    max_results: int | None = 5,
    sort_by: str | None = None,
    sort_order: str | None = None 
):
    # Create dictionary of given arguments (filter out None)
    query_params = {key: value for key, value in locals().items() if value is not None} # locals() gets all local variables

    # Check that at least one argument is provided
    if not query_params:
        raise HTTPException(
            status_code=400,
            detail='Provide at least one query parameter.'
        )

    # Make concurrent calls
    # arxiv_data, elsevier_data, ieee_data = await asyncio.gather(fetch_arxiv(), fetch_elsevier(), fetch_ieee())

    arxiv_data = await fetch_arxiv(**query_params)
    
    return {'arxiv': arxiv_data}
