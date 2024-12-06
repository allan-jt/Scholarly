from .setup import RedisSingleton


async def initialize_redis():
    redisInstance = RedisSingleton()
    return await redisInstance.initialize()


async def close_redis():
    redisInstance = RedisSingleton()
    return await redisInstance.close()


def get_redis_results():
    redisInstance = RedisSingleton()
    return redisInstance.get_redis_results()


def get_redis_chunks():
    redisInstance = RedisSingleton()
    return redisInstance.get_redis_chunks()


__all__ = ["initialize_redis", "close_redis", "get_redis_results", "get_redis_chunks"]
