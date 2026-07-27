from src.config.config import settings
import asyncio
from aiogram import Bot, Dispatcher
from front.handlers.routes import router

dp = Dispatcher()

async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    print("Started")
    await dp.start_polling(bot)

dp.include_router(router)

if __name__ == "__main__":
    asyncio.run(main())