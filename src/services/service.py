from src.repository.repository import WordRepository
from sqlalchemy.orm import Session
from src.schemas.dict_schema import WordCreate, WordSchema,  WordDelete, WordGet
from src.third_party.translate_api import get_translated_text
from sqlalchemy.ext.asyncio import AsyncSession
from src.exceptions import WordIsAlreadyExist, WordIsNotExists
from src.third_party.llm_api import get_examples_from_local_llm
from src.cache.cache import RedisCacheBack


from redis.asyncio import Redis


class WordService:
    def __init__(self, db: AsyncSession, redis: Redis):
        self.db = db
        self.word_repository = WordRepository(db=self.db)
        self.aioredis_client = RedisCacheBack(redis_client=redis)
        self.word_key = "dict:words:" # + user_id

    #создание слова
    async def word_create_new(self, word: WordCreate):
        
        key = await self.aioredis_client.get_key(self.word_key, word.user_id)
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
    async def word_create(self, word: WordCreate):
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
    async def word_list(self):
        cache_list = await self.aioredis_client.get(self.word_key)
        if cache_list:
            return cache_list
        
        word_list_orm = await self.word_repository.get_all()

        words: list[WordSchema] = [WordSchema.model_validate(word) for word in word_list_orm]
        words_for_cache = [word.model_dump() for word in words]

        await self.aioredis_client.set(self.word_key, words_for_cache)

        return words
    #список слов конкретного пользователя
    async def word_by_user_list(self, user_id:str):

        key = await self.aioredis_client.get_key(self.word_key, user_id)
        cache_words = await self.aioredis_client.get(key)
        if cache_words:
            return cache_words
        
        word_list_orm = await self.word_repository.get_all_by_user(user_id=user_id)

        words: list[WordSchema] = [WordSchema.model_validate(word) for word in word_list_orm]
        words_for_cache = [word.model_dump() for word in words]
        
        await self.aioredis_client.set(key, words_for_cache)

        return words
    #удаление слова
    async def word_delete(self, word_to_delete: WordDelete):
        #cache
        key = await self.aioredis_client.get_key(self.word_key, word_to_delete.user_id)
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
    async def get_word(self, word_to_get: WordGet):
        #Кэш
        key = await self.aioredis_client.get_key(self.word_key, word_to_get.user_id)
        cache_list = await self.aioredis_client.get(key=key)
        if cache_list:
            word = await self.aioredis_client.is_in_cache(cache_list, word_to_get.body)
            if word:
                response = {"translate": word["translate"], "examples": word["examples"]}
                return response

        #через бд
        if await self.word_repository.word_is_exist(word=word_to_get):
            word = await self.word_repository.get_by_user_id_body(word_to_get)
            response = {"translate": word.translate, "examples": word.examples}
            return response
        examples = await get_examples_from_local_llm(word_to_get.body)
        examples = examples["examples"]
        translate = await get_translated_text(word_to_get.body)
        response = {"translate": translate, "examples": examples}
        return response