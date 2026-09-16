from fastapi import APIRouter, Depends, HTTPException, status

from exceptions import AllWordsPassed
from schemas.game_schemas import WordForGame

from api.depends import get_word_service

from services.service import WordService


router = APIRouter(prefix="/game")

@router.get("/{user_id}")
async def get_game_word(user_id: str, word_service: WordService = Depends(get_word_service)) -> WordForGame:
    try:
        word: WordForGame = await word_service.get_game_word(user_id)
    except AllWordsPassed as e:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=str(e)
            )
    return word

@router.post("/{user_id}/{word_id}")
async def add_wrong_word(user_id: str, word_id:str, word_service: WordService = Depends(get_word_service)) -> None:
    return await word_service.add_wrong_word(user_id, word_id)

@router.get("/wrong/{user_id}")
async def get_user_wrong_words(user_id: str, word_service: WordService = Depends(get_word_service)) -> list[WordForGame] | list:
    words = await word_service.get_user_wrong_words(user_id)
    return words
