from fastapi import Depends
from src.db.session import get_db
from src.services.service import WordService
from sqlalchemy.ext.asyncio import AsyncSession

async def get_word_service(db: AsyncSession = Depends(get_db)) -> WordService:
    return WordService(db=db)