import asyncio
import aiohttp
from fastapi import HTTPException


async def fetch_single_pdf(pdf_link: str) -> bytes:
    """
    Fetches the binary content of a single PDF from the given URL.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(pdf_link) as response:
            if response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail={
                        "error": "Failed to fetch PDF from the source.",
                        "instance": pdf_link,
                    },
                )
            return await response.read()  # Return binary content of the PDF
