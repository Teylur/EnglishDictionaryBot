from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session

from src.schemas.dict_schema import WordCreate, WordSchema
from src.db.session import get_db
from src.api.depends import get_word_service

from src.services.service import WordService


router = APIRouter(prefix="/dict")

@router.post("", status_code=status.HTTP_201_CREATED)
def word_create(payload: WordCreate, word_service: WordService = Depends(get_word_service)) -> WordSchema:
    return word_service.word_create(payload)

@router.get("")
def word_list(word_service: WordService = Depends(get_word_service)) -> list[WordSchema]:
    return word_service.word_list()

@router.delete("/{word_id}", status_code=status.HTTP_204_NO_CONTENT)
def word_delete(word_id: str, word_service: WordService = Depends(get_word_service)) -> None:
    word_service.word_delete(word_id=word_id)
