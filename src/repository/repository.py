from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from src.schemas.dict_schema import WordCreate, WordDelete, WordGet
from src.models.word_orm import WordORM

class WordRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        word_list = self.db.scalars(select(WordORM)).all()
        return word_list
    def get_all_by_user(self, user_id: str):
            word_list = self.db.query(WordORM).filter(WordORM.user_id == user_id)
            return word_list

    def get_by_id(self, word_id: str) -> WordORM:
        return self.db.get(WordORM, word_id)

    def get_by_user_id_body(self, word: WordDelete | WordGet)-> WordORM:
        return self.db.query(WordORM).filter(WordORM.body == word.body, WordORM.user_id == word.user_id).one()

    async def word_is_exist(self, word: WordCreate | WordDelete | WordGet):
        request = select(exists().where(
            WordORM.body == word.body,
            WordORM.user_id == word.user_id
        ))
        result = self.db.execute(request)
        return result.scalar()

    async def create(self, word: WordCreate):
        new_word = WordORM(body=word.body, translate=word.translate, user_id=word.user_id, examples=word.examples)
        self.db.add(new_word)
        return new_word

    def delete(self, word: WordDelete):
        word_to_delete = self.get_by_user_id_body(word)
        self.db.delete(word_to_delete)
    