from contextlib import asynccontextmanager

from fastapi import FastAPI
from src.models.base import Base
from src.db.session import engine
from src.api.routes.dict_roter import router as dict_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield 

app = FastAPI(lifespan=lifespan)

app.include_router(dict_router)