from src.repository.repository import WordRepository
from sqlalchemy.orm import Session
from src.schemas.dict_schema import WordCreate, WordSchema,  WordDelete, WordGet
from src.third_party.translate_api import get_translated_text
import asyncio
from src.exceptions import WordIsAlreadyExist, WordIsNotExists
from src.third_party.llm_api import get_examples_from_local_llm

class WordService:
    def __init__(self, db: Session):
        self.db = db
        self.word_repository = WordRepository(db=self.db)

    async def word_create_new(self, word: WordCreate):
        if await self.word_repository.word_is_exist(word=word):
            raise WordIsAlreadyExist(word=word.body)
        new_word = await self.word_repository.create(word)
        self.db.commit()
        self.db.flush()
        return WordSchema.model_validate(new_word)
        
            

    async def word_create(self, word: WordCreate):
        if await self.word_repository.word_is_exist(word=word):
            raise WordIsAlreadyExist(word=word.body)
        examples = await get_examples_from_local_llm(word.body)
        word.examples = examples["examples"]
        word.translate = await get_translated_text(word.body)
        new_word = await self.word_repository.create(word)
        self.db.commit()
        self.db.flush()
        return WordSchema.model_validate(new_word)

    def word_list(self):
        word_list_orm = self.word_repository.get_all()
        return [WordSchema.model_validate(word) for word in word_list_orm]
    
    def word_by_user_list(self, user_id:str):
        word_list_orm = self.word_repository.get_all_by_user(user_id=user_id)
        return [WordSchema.model_validate(word) for word in word_list_orm]

    async def word_delete(self, word_to_delete: WordDelete):
        if not await self.word_repository.word_is_exist(word=word_to_delete):
            raise WordIsNotExists(word=word_to_delete)
        self.word_repository.delete(word_to_delete)
        self.db.commit()

    async def get_word(self, word_to_get: WordGet):
        if await self.word_repository.word_is_exist(word=word_to_get):
            print("Penis")
            word = self.word_repository.get_by_user_id_body(word_to_get)
            response = {"translate": word.translate, "examples": word.examples}
            return response
        examples = await get_examples_from_local_llm(word_to_get.body)
        examples = examples["examples"]
        translate = await get_translated_text(word_to_get.body)
        response = {"translate": translate, "examples": examples}
        return response