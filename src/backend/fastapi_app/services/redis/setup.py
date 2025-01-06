import aioredis
import os
from .process_status import ProcessStatus
import json


class RedisSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisSingleton, cls).__new__(cls)
            cls._instance.pdf_summary = None  # {pdf_link: summary}
            cls._instance.pdf_process_status = None  # {pdf_link: status}
        return cls._instance

    async def initialize(self) -> None:
        if not self.pdf_summary:
            self.pdf_summary = await aioredis.from_url(f'{os.environ["REDIS_URL"]}/0')
        if not self.pdf_process_status:
            self.pdf_process_status = await aioredis.from_url(
                f'{os.environ["REDIS_URL"]}/1'
            )

    async def get_pdf_summary(self, pdf_link: str) -> dict:
        data = await self.pdf_summary.get(pdf_link)
        if data is None:
            return None
        return json.loads(data)

    async def store_pdf_summary(self, pdf_link: str, summary: dict) -> None:
        await self.pdf_summary.set(pdf_link, json.dumps(summary), ex=60)

    async def get_pdf_process_status(self, pdf_link: str) -> ProcessStatus:
        status = await self.pdf_process_status.get(pdf_link)
        if status is None:
            return None
        return ProcessStatus[status.decode()]

    async def store_pdf_process_status(
        self, pdf_link: str, status: ProcessStatus
    ) -> None:
        await self.pdf_process_status.set(pdf_link, status.name, ex=60)

    async def clear_and_close(self, redis_db: aioredis.Redis) -> None:
        if redis_db:
            await redis_db.flushdb()
            await redis_db.close()

    async def close(self) -> None:
        await self.clear_and_close(self.pdf_summary)
        await self.clear_and_close(self.pdf_process_status)
