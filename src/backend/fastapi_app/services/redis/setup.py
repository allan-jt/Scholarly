import aioredis
import os
from .process_status import ProcessStatus


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
        redis_hash = await self.pdf_summary.hgetall(pdf_link)
        return {k.decode(): v.decode() for k, v in redis_hash.items()}

    async def store_pdf_summary(self, pdf_link: str, summary: dict) -> None:
        await self.pdf_summary.hset(pdf_link, mapping=summary)
        await self.pdf_summary.expire(pdf_link, 3600)  # expire in 1 hour

    async def get_pdf_process_status(self, pdf_link: str) -> ProcessStatus:
        return await self.pdf_process_status.get(pdf_link)

    async def store_pdf_process_status(
        self, pdf_link: str, status: ProcessStatus
    ) -> None:
        await self.pdf_process_status.set(pdf_link, status, expire=3600)

    async def clear_and_close(self, redis_db: aioredis.Redis) -> None:
        if redis_db:
            await redis_db.flushdb()
            await redis_db.close()

    async def close(self) -> None:
        await self.clear_and_close(self.pdf_summary)
        await self.clear_and_close(self.pdf_process_status)
