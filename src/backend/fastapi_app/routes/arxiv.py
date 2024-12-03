from fastapi import APIRouter, HTTPException
import aiohttp
import xmltodict

router = APIRouter()

@router.get('/')
async def fetch_arxiv(
    title: str | None = None,
    author: str | None = None,
    abstract: str | None = None,
    comment: str | None = None,
    journal_reference: str | None = None,
    subject_category: str | None = None,
    report_number: str | None = None,
    all: str | None = None,
    id_list: str | None = None,
    boolean_operator: str | None = 'AND',   # AND, OR, ANDNOT
    start: int | None = 0,
    max_results: int | None = 5,
    sort_by: str | None = None,             # relevance, lastUpdatedDate, submittedDate
    sort_order: str | None = None           # ascending, descending
):
    base_url = 'http://export.arxiv.org/api/query'
    
    # Prefix mappings for search query fields
    prefixes = {
        'title': 'ti',
        'author': 'au',
        'abstract': 'abs',
        'comment': 'co',
        'journal_reference': 'jr',
        'subject_category': 'cat',
        'report_number': 'rn',
        'all': 'all'
    }

    request_args = locals()

    # Construct search query with encodings
    search_query_parts = [
        f'{prefixes[key]}:%22{value.replace(" ", "+")}%22'  # encode quotes as %22 and space as +
        for key, value in request_args.items()
        if key in prefixes.keys() and value is not None     # filter for search_query args
    ]
    search_query = f'+{boolean_operator}+'.join(search_query_parts)

    # Construct final query parameters
    query_params = {
        'search_query': search_query,
        'id_list': id_list,
        'start': start,
        'max_results': max_results,
        'sortBy': sort_by,
        'sortOrder': sort_order
    }
    query_string = '&'.join(f'{key}={value}' for key, value in query_params.items() if value is not None)

    # Create full URL
    url = f'{base_url}?{query_string}'

    # Make asynchronous HTTP call
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail={
                        'error': 'Failed to fetch data from arXiv API.',
                        'instance': url
                    }
                )
            xml_response = await response.text()

    # Convert XML response to JSON
    data = xmltodict.parse(xml_response)

    return data
