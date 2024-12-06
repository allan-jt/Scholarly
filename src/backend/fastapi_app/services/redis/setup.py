import aioredis


class RedisSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisSingleton, cls).__new__(cls)
            cls._instance.results = None
            cls._instance.chunks = None
        return cls._instance

    async def initialize(self) -> None:
        if not self.results:
            self.results = await aioredis.from_url("redis://redis:6379/0")
        if not self.chunks:
            self.chunks = await aioredis.from_url("redis://redis:6379/1")

    async def close(self) -> None:
        if self.results:
            await self.results.close()
        if self.chunks:
            await self.chunks.close()

    def get_redis_results(self) -> aioredis.Redis:
        return self.results

    def get_redis_chunks(self) -> aioredis.Redis:
        return self.chunks
