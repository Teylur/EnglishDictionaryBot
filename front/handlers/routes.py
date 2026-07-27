from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def hello(message: Message):
    await message.answer(
        "Твой личный *словарь* английских слов\nСписок комманд /help",
        parse_mode="Markdown" # можно HTML
        )

@router.message(Command("help"))
async def help(message: Message):
    await message.answer("Комманды:\n/dict - словарь\n/play - играть в игру")

@router.message(Command("dict"))
async def dict(message: Message):
    await message.answer("словарь")

@router.message(Command("play"))
async def help(message: Message):
    await message.answer("Играть")
