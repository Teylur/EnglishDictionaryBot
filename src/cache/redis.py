import redis.asyncio as aioredis
from src.config.config import settings

redis_client: aioredis.Redis

async def redis_init():
    global redis_client
    redis_client = aioredis.Redis.from_url(
        settings.REDIS_URL,
        decode_responses=True,
        encoding="utf-8"
    )
    await redis_client.ping()
    print("Redis is working")

async def redis_close():
    global redis_client
    if redis_client:
        redis_client.close()
    print("Redis closed")

async def get_redis():
    if redis_client:
        return redis_client
    print("Redis isn't working")
    