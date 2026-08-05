from src.config.config import settings
import asyncio
from aiogram import Bot, Dispatcher
from front.handlers.base import router as base_router
from front.handlers.dictionary import router as dictionary_router
from front.handlers.game import router as game_router

dp = Dispatcher()

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    print("Started")
    await dp.start_polling(bot)

dp.include_router(base_router)
dp.include_router(dictionary_router)
dp.include_router(game_router)

if __name__ == "__main__":
    asyncio.run(main())