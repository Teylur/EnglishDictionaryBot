from fastapi import Depends
from src.db.session import get_db
from src.services.service import WordService
from sqlalchemy.orm import Session

def get_word_service(db: Session = Depends(get_db)) -> WordService:
    return WordService(db=db)