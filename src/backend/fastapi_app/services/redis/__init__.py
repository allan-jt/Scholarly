from .setup import RedisSingleton, aioredis


async def initialize_redis() -> None:
    redisInstance = RedisSingleton()
    await redisInstance.initialize()


async def close_redis() -> None:
    redisInstance = RedisSingleton()
    await redisInstance.close()


def get_redis_results() -> aioredis.Redis:
    redisInstance = RedisSingleton()
    return redisInstance.get_redis_results()


def get_redis_chunks() -> aioredis.Redis:
    redisInstance = RedisSingleton()
    return redisInstance.get_redis_chunks()


__all__ = ["initialize_redis", "close_redis", "get_redis_results", "get_redis_chunks"]
