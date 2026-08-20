from fastapi import APIRouter, status, Depends, HTTPException

from src.schemas.dict_schema import WordCreate, WordSchema, WordDelete, WordGet
from src.api.depends import get_word_service

from src.services.service import WordService

from src.exceptions import WordIsAlreadyExist, WordIsNotExists


router = APIRouter(prefix="/dict")

@router.post("", status_code=status.HTTP_201_CREATED)
async def word_create(payload: WordCreate, word_service: WordService = Depends(get_word_service)) -> WordSchema:
    try:
        new_word = await word_service.word_create_new(payload)
    except WordIsAlreadyExist as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    return new_word



@router.get("/")
async def word_list(word_service: WordService = Depends(get_word_service)) -> list[WordSchema]:
    return await word_service.word_list()

@router.get("/{user_id}")
async def word_list(user_id: str, word_service: WordService = Depends(get_word_service)) -> list[WordSchema]:
    return await word_service.word_by_user_list(user_id=user_id)

@router.get("/{user_id}/{word_body}")
async def get_word(user_id:str, word_body: str, word_service: WordService = Depends(get_word_service)) -> dict[str, str | list[dict[str, str]]]:
    word = WordGet(body=word_body, user_id=user_id)
    print(word)
    return await word_service.get_word(word)

@router.delete("/{user_id}/{word_body}", status_code=status.HTTP_204_NO_CONTENT)
async def word_delete(user_id: str, word_body: str, word_service: WordService = Depends(get_word_service)) -> None:
    word_to_delete = WordDelete(user_id=user_id, body=word_body)
    try:
        await word_service.word_delete(word_to_delete)
    except WordIsNotExists as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
