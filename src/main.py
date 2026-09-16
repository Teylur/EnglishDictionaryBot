from contextlib import asynccontextmanager

from fastapi import FastAPI
from models.base import Base
from db.session import engine
from api.routes.dict_roter import router as dict_router
from api.routes.game_router import router as game_router
from cache.redis import redis_init, redis_close

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await redis_init()
    yield 
    await redis_close()

app = FastAPI(lifespan=lifespan)

app.include_router(dict_router)

app.include_router(game_router)