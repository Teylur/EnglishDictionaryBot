from sqlalchemy import select
from sqlalchemy.orm import Session
from src.schemas.dict_schema import WordCreate
from src.models.word_orm import WordORM

class WordRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        word_list = self.db.scalars(select(WordORM)).all()
        return word_list

    def get_by_id(self, word_id: str) -> WordORM:
        return self.db.get(WordORM, word_id)

    def create(self, word: WordCreate):
        new_word = WordORM(body=word.body)
        self.db.add(new_word)
        return new_word

    def delete(self, word_id: str):
        word_to_delete = self.get_by_id(word_id)
        self.db.delete(word_to_delete)
    