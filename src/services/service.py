from src.repository.repository import WordRepository
from sqlalchemy.orm import Session

from src.schemas.dict_schema import WordCreate, WordSchema,  WordDelete, WordGet
from src.schemas.game_schemas import WordForGame

from src.third_party.translate_api import get_translated_text
from sqlalchemy.ext.asyncio import AsyncSession
from src.exceptions import AllWordsPassed, HashIsAlreadyExists, WordIsAlreadyExist, WordIsNotExists, LLMRequestsLimit
from src.third_party.llm_api import get_examples_from_local_llm
from src.cache.cache import RedisCacheBack
from src.config.config import settings


from redis.asyncio import Redis


class WordService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.word_repository = WordRepository(db=self.db)
        self.aioredis_client = RedisCacheBack(redis_client=redis)

        self.dict_word_key = "dict:words:" # + user_id

        self.game_word_key = "game:words:" # + user_id
        self.game_ttl = 120

        self.llm_ttl = settings.LLM_REQUESTS_TTL
        self.llm_requests_limit = settings.LLM_REQUESTS_LIMIT

    #создание слова
    async def word_create_new(self, word: WordCreate) -> WordSchema:
        
        key = await self.aioredis_client.get_key(self.dict_word_key, word.user_id)
        cache_list = await self.aioredis_client.get(key=key)

        #проверка есть ли в кэше
        if cache_list:
            if await self.aioredis_client.is_in_cache(cache_list, word.body):
                raise WordIsAlreadyExist(word=word.body)
        
        #очищаем кэш
        await self.aioredis_client.delete(key=key)

        if await self.word_repository.word_is_exist(word=word):
            raise WordIsAlreadyExist(word=word.body)
        
        new_word = await self.word_repository.create(word)
        await self.db.commit()
        await self.db.flush()
        return WordSchema.model_validate(new_word)
        
            
    #old version of creation
    async def word_create(self, word: WordCreate) -> WordSchema:
        if await self.word_repository.word_is_exist(word=word):
            raise WordIsAlreadyExist(word=word.body)
        examples = await get_examples_from_local_llm(word.body)
        word.examples = examples["examples"]
        word.translate = await get_translated_text(word.body)
        new_word = await self.word_repository.create(word)
        await self.db.commit()
        await self.db.flush()
        return WordSchema.model_validate(new_word)

    #список всех слов
    async def word_list(self) -> list[WordSchema]:
        cache_list = await self.aioredis_client.get(self.dict_word_key)
        if cache_list:
            return cache_list
        
        word_list_orm = await self.word_repository.get_all()

        words: list[WordSchema] = [WordSchema.model_validate(word) for word in word_list_orm]
        words_for_cache = [word.model_dump() for word in words]

        await self.aioredis_client.set(self.dict_word_key, words_for_cache)

        return words
    #список слов конкретного пользователя
    async def word_by_user_list(self, user_id:str) -> list[WordSchema]:

        key = await self.aioredis_client.get_key(self.dict_word_key, user_id)
        cache_words = await self.aioredis_client.get(key)
        if cache_words:
            return cache_words
        
        word_list_orm = await self.word_repository.get_all_by_user(user_id=user_id)

        words: list[WordSchema] = [WordSchema.model_validate(word) for word in word_list_orm]
        words_for_cache = [word.model_dump() for word in words]
        
        await self.aioredis_client.set(key, words_for_cache)

        return words
    #удаление слова
    async def word_delete(self, word_to_delete: WordDelete) -> None:
        #cache
        key = await self.aioredis_client.get_key(self.dict_word_key, word_to_delete.user_id)
        cache_list = await self.aioredis_client.get(key)
        if cache_list:
            word = await self.aioredis_client.is_in_cache(cache_list, word_to_delete.body)
            if word:
                raise WordIsNotExists(word=word_to_delete)

        if not await self.word_repository.word_is_exist(word=word_to_delete):
            raise WordIsNotExists(word=word_to_delete)
        #очистка кэша
        await self.aioredis_client.delete(key=key)

        await self.word_repository.delete(word_to_delete)
        await self.db.commit()
    #получение слова
    async def get_word(self, word_to_get: WordGet) -> dict[str, str]:
        #Cache
        key1 = await self.aioredis_client.get_key(self.dict_word_key, word_to_get.user_id)

        # llm requests limit  
        key2 = await self.aioredis_client.get_key(self.dict_word_key, word_to_get.user_id, "llm_request") 
        if not await self.aioredis_client.is_in_request_limit(key2, self.llm_requests_limit, self.llm_ttl):
            raise LLMRequestsLimit(self.llm_requests_limit, self.llm_ttl)
        
        cache_list = await self.aioredis_client.get(key=key1)
        if cache_list:
            word = await self.aioredis_client.is_in_cache(cache_list, word_to_get.body)
            if word:
                response = {"translate": word["translate"], "examples": word["examples"]}
                return response

        #through DB
        if await self.word_repository.word_is_exist(word=word_to_get):
            word = await self.word_repository.get_by_user_id_body(word_to_get)
            response = {"translate": word.translate, "examples": word.examples}
            return response
        
        # generate
        examples = await get_examples_from_local_llm(word_to_get.body)
        examples = examples["examples"]
        translate = await get_translated_text(word_to_get.body)
        response = {"translate": translate, "examples": examples}
        return response

    #Game

    async def get_game_word(self, user_id: str) -> WordForGame:

        key = await self.aioredis_client.get_key(self.game_word_key, user_id=user_id)

        word = await self.aioredis_client.next_word(key=key)

        if not word:
            words = await self.word_repository.get_all_by_user(user_id)
            try:
                word = await self.aioredis_client.set_set_hash(key, words, self.game_ttl)
            except HashIsAlreadyExists:
                raise AllWordsPassed()
            return WordForGame.model_validate(word)
        
        return WordForGame.model_validate(word)

    async def add_wrong_word(self, user_id:str , word_id:str) -> None:
        key = await self.aioredis_client.get_key(self.game_word_key, user_id=user_id)

        await self.aioredis_client.add_wrong_word(key, word_id, self.game_ttl)

    async def get_user_wrong_words(self, user_id: str) -> list[WordForGame]:
        key = await self.aioredis_client.get_key(self.game_word_key, user_id=user_id)

        words = await self.aioredis_client.get_wrong_words(key)

        
        if words:
            print(words)
            return [WordForGame.model_validate(word) for word in words]
        return []

