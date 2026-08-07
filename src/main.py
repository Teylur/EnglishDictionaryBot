from contextlib import asynccontextmanager

from fastapi import FastAPI, status
from src.models.base import Base
from src.schemas.dict_schema import WordCreate
from src.db.session import engine
from src.api.routes.dict_roter import router as dict_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(dict_router)