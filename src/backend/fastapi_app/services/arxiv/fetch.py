from fastapi import HTTPException
import aiohttp
import xmltodict

async def fetch(query_fields: dict, query_config: dict) -> dict:
    base_url = 'http://export.arxiv.org/api/query'

    # Extract keys from query_fields and query_config
    id_list = query_fields.pop('id', None)                  # id_list is handled separately from other query fields
    boolean_operator = query_config.pop('boolean_operator') # boolean_operator is only used for query construction

    # Construct encoded search query
    query_field_encodings = [
        f'{key}:%22{value.replace(" ", "+")}%22'   # encode quotes as %22 and space as +
        for key, value in query_fields.items()
    ]
    search_query = f'+{boolean_operator}+'.join(query_field_encodings)

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
