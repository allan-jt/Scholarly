from fastapi import HTTPException
import aiohttp
import xmltodict
from models.arxiv import QueryPrefixes, QueryConfig

async def fetch(
    prefixes: QueryPrefixes,
    config: QueryConfig
):
    base_url = 'http://export.arxiv.org/api/query'

    # Mapping of field names to arXiv API query prefixes
    prefix_mappings = {
        'title': 'ti',
        'author': 'au',
        'abstract': 'abs',
        'comment': 'co',
        'journal_reference': 'jr',
        'subject_category': 'cat',
        'report_number': 'rn',
        'all': 'all'
    }

    # Convert prefix and config models to dictionaries
    query_prefixes = prefixes.model_dump(exclude_none=True)
    query_config = config.model_dump(exclude_none=True)

    # Extract fields from query_prefixes and query_config
    id_list = query_prefixes.pop('id_list', None)           # id_list is handled separately from other prefixes
    boolean_operator = query_config.pop('boolean_operator') # boolean_operator is only used for query construction

    # Construct encoded search query
    query_prefix_encodings = [
        f'{prefix_mappings[key]}:%22{value.replace(" ", "+")}%22'   # encode quotes as %22 and space as +
        for key, value in query_prefixes.items()
    ]
    search_query = f'+{boolean_operator}+'.join(query_prefix_encodings)

    # Construct final query parameters
    query_params = {
        'search_query': search_query,
        'id_list': id_list,
        **query_config
    }
    query_string = '&'.join(f'{key}={value}' for key, value in query_params.items() if value is not None)

    # Construct full URL for arXiv API request
    url = f'{base_url}?{query_string}'

    # Make asynchronous HTTP GET request to arXiv API
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

    # Parse XML response into JSON
    data = xmltodict.parse(xml_response)

    return data
