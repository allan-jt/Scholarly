from fastapi import APIRouter, HTTPException, Depends
import asyncio
from models.arxiv import QueryPrefixes, QueryConfig
from services import arxiv

router = APIRouter()

@router.get('')
async def query(
    prefixes: QueryPrefixes = Depends(),
    config: QueryConfig = Depends()
):
    # Check that 'all' prefix argument is provided
    if not prefixes.all:
        raise HTTPException(
            status_code=400,
            detail="The 'all' prefix field is required."
        )

    arxiv_data = await arxiv.fetch(prefixes, config)    # need to filter out other prefixes

    return {'arxiv': arxiv_data}

@router.get('/advanced')
async def query_advanced(
    prefixes: QueryPrefixes = Depends(),
    config: QueryConfig = Depends()
):
    # Check that at least one prefix argument is provided
    if not prefixes.model_dump(exclude_none=True):
        raise HTTPException(
            status_code=400,
            detail='At least one prefix field is required.'
        )

    # Make concurrent calls
    # arxiv_data, elsevier_data, ieee_data = await asyncio.gather(arxiv.fetch(), elsevier.fetch(), ieee.fetch())

    arxiv_data = await arxiv.fetch(prefixes, config)    # need to filter out 'all' prefix
    
    return {'arxiv': arxiv_data}
