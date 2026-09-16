from fastapi import Depends
from db.session import get_db
from services.service import WordService
from sqlalchemy.ext.asyncio import AsyncSession

from redis.asyncio  import Redis
from cache.redis import get_redis

async def get_word_service(db: AsyncSession = Depends(get_db), redis: Redis = Depends(get_redis)) -> WordService:
    return WordService(db=db, redis=redis)