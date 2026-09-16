from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from httpx import AsyncClient
import httpx
from states.states import Dictionary, GameMode
from keyboards.dict_keyboards import get_dict_main_Readline_keyboard
from config.config import settings

router = Router()

@router.message(Command("start"))
async def hello(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Твой личный *словарь* английских слов\nСписок комманд /help",
        parse_mode="Markdown", # можно HTML
        reply_markup=get_dict_main_Readline_keyboard()
        )
    await state.set_state(Dictionary.word)

@router.message(Command("help"))
async def help(message: Message):
    await message.answer("Комманды:\n/dict - словарь\n/play - играть в игру")

@router.message(Command("dict"))
async def dict(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("словарь")
    await state.set_state(Dictionary.word)

@router.message(Command("play"))
async def play(message: Message, state: FSMContext):
    await state.clear()
    user_id = str(message.from_user.id)
    async with AsyncClient() as client:
        r: httpx.Response = await client.get(url=f'{settings.BACKEND_URL}/game/{user_id}')
    response = r.json()
    await state.update_data(response)
    await message.answer("Переведите слово: " + response["body"])
    await state.set_state(GameMode.waiting_for_answer)
    

