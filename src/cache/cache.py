from redis import asyncio
from src.exceptions import HashIsAlreadyExists
from src.cache.redis import get_redis
import json

class RedisCacheBack:
    def __init__(self, redis_client: asyncio.Redis):
        self.redis_client = redis_client

        self.wrong_words_key_set = ":wrong:set"
    
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

    async def get_key(self, pure_key:str, user_id:str, action: str = '') -> str:
        key = pure_key+user_id + action
        return key

    async def is_in_cache(self, cache_list:dict[any, any], word_body:str):
        for body in cache_list:
            if word_body == body["body"]:
                return body
        return False

    async def is_in_request_limit(self, key, limit, window):
        current_requests = await self.redis_client.incr(key)
        print("ЧИСЛО ЗАПРОСОВ:", current_requests)

        if current_requests == 1:
            # print("ЗАШЛО СЮДА")
            await self.redis_client.expire(key, window)

        if current_requests > limit:
            return False
        return True

    #Game

    async def set_set_hash(self, key: str, data, ttl) -> dict:
        key_for_set = key+":set"
        key_for_hash = key+":hash"
        words_id = []
        mapped_hash = {}
        for word in data:
            words_id.append(word.id)
            mapped_hash[word.id] =  json.dumps({"id": word.id, "body": word.body, "translate": word.translate}, ensure_ascii=False)

        await self.redis_client.sadd(key_for_set, *words_id)
        is_exist = await self.redis_client.exists(key_for_hash)
        await self.redis_client.hset(key_for_hash, mapping=mapped_hash)

        await self.redis_client.expire(key_for_set, ttl)
        await self.redis_client.expire(key_for_hash, ttl)

        if is_exist:
            raise HashIsAlreadyExists

        

        return await self.next_word(key)

    async def next_word(self, key: str) -> list[dict, str]:
        key_for_set = key+":set"
        key_for_hash = key+":hash"
        word_id = await self.redis_client.spop(key_for_set)
        if not word_id:
            return False
        word = await self.redis_client.hget(key_for_hash, word_id)
        return json.loads(word)

    async def add_wrong_word(self, key: str, word_id: str, ttl):
        key = key+self.wrong_words_key_set
        is_exist = await self.redis_client.exists(key)
        await self.redis_client.sadd(key, word_id)

        if not is_exist:
            print(f"ПОСТАВИЛ TTL {ttl} секунд")
            await self.redis_client.expire(key, ttl)

    async def get_wrong_words(self, key: str) -> list[dict]:
        key1 = key+self.wrong_words_key_set
        key2 = key + ":hash"

        words_id = await self.redis_client.smembers(key1)
        if words_id:
            print(words_id)
            words = await self.redis_client.hmget(key2, *words_id)
            await self.redis_client.unlink(key1)
            return [json.loads(word) for word in words] 
        return []
        





        
        
            

