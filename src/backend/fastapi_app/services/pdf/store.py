import asyncio
import aiohttp
from fastapi import HTTPException


async def fetch(session: aiohttp.ClientSession, pdf_link: str) -> bytes:
    async with session.get(pdf_link) as response:
        # print(response)
        if response.status != 200:
            raise HTTPException(
                status_code=response.status,
                detail={
                    "error": "Failed to fetch PDF from arXiv site.",
                    "instance": pdf_link,
                },
            )
        return await response.read()  # read and return binary content


# async def store_in_redis(req_id: str, pdf_links: list[str]) -> None:
#     # Get Redis connection
#     redis_db = get_redis_pdfs()

#     # Make concurrent calls to fetch PDFs
#     async with aiohttp.ClientSession() as session:
#         tasks = []
#         for pdf_link in pdf_links:
#             task = asyncio.create_task(fetch(session, pdf_link))
#             tasks.append(task)
#         pdf_contents = await asyncio.gather(*tasks)

#     # Store fetched PDF contents in Redis
#     await redis_db.rpush(req_id, *pdf_contents)
