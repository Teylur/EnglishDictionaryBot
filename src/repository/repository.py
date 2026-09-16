from sqlalchemy import select, exists
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.dict_schema import WordCreate, WordDelete, WordGet
from models.word_orm import WordORM

class WordRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        word_list = await self.db.execute(select(WordORM))
        return word_list.scalars().all()
    async def get_all_by_user(self, user_id: str):
            stmt = select(WordORM).where(WordORM.user_id == user_id)
            word_list = await self.db.execute(stmt)
            return word_list.scalars().all()

    async def get_by_id(self, word_id: str) -> WordORM:
        return await self.db.get(WordORM, word_id)

    async def get_by_user_id_body(self, word: WordDelete | WordGet)-> WordORM:
        stmt = select(WordORM).where(WordORM.body == word.body, WordORM.user_id == word.user_id)
        result = await self.db.execute(stmt)
        return result.scalar()

    async def word_is_exist(self, word: WordCreate | WordDelete | WordGet):
        request = select(exists().where(
            WordORM.body == word.body,
            WordORM.user_id == word.user_id
        ))
        result = await self.db.execute(request)
        return result.scalar()

    async def create(self, word: WordCreate):
        new_word = WordORM(body=word.body, translate=word.translate, user_id=word.user_id, examples=word.examples)
        self.db.add(new_word)
        return new_word

    async def delete(self, word: WordDelete):
        word_to_delete = await self.get_by_user_id_body(word)
        await self.db.delete(word_to_delete)
    