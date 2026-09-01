from redis import asyncio
from src.cache.redis import get_redis
import json

class RedisCacheBack:
    def __init__(self, redis_client: asyncio.Redis):
        self.redis_client = redis_client
    
    async def set(self, key: str, data) -> None:
        # ex - время существования кэша в секундах
        await self.redis_client.set(key, json.dumps(data), ex=3600)

    async def get(self, key:str) -> dict:
        data: str = await self.redis_client.get(key)
        if data != None:
            return json.loads(data)
        return None

    async def delete(self, key: str) -> None:
        await self.redis_client.delete(key)

    async def get_key(self, pure_key:str, user_id:str) -> str:
        key = pure_key+user_id
        return key

    async def is_in_cache(self, cache_list:dict[any, any], word_body:str):
        for body in cache_list:
            if word_body == body["body"]:
                return body
        return False
        
            

