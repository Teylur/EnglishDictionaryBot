from src.repository.repository import WordRepository
from sqlalchemy.orm import Session
from src.schemas.dict_schema import WordCreate, WordSchema
from src.third_party.translate_api import get_translated_text
import asyncio
from src.exceptions import WordIsAlreadyExist
from src.third_party.llm_api import get_examples_from_local_llm

class WordService:
    def __init__(self, db: Session):
        self.db = db
        self.word_repository = WordRepository(db=self.db)

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

    def word_delete(self, word_id: str):
        self.word_repository.delete(word_id=word_id)
        self.db.commit()