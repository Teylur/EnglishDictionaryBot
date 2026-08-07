from src.repository.repository import WordRepository
from sqlalchemy.orm import Session
from src.schemas.dict_schema import WordCreate, WordSchema

class WordService:
    def __init__(self, db: Session):
        self.db = db
        self.word_repository = WordRepository(db=self.db)

    def word_create(self, word: WordCreate):
        new_word = self.word_repository.create(word)
        self.db.commit()
        return WordSchema.model_validate(new_word)

    def word_list(self):
        word_list_orm = self.word_repository.get_all()
        return [WordSchema.model_validate(word) for word in word_list_orm]

    def word_delete(self, word_id: str):
        self.word_repository.delete(word_id=word_id)
        self.db.commit()