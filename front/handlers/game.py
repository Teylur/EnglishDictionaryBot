from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from front.states.states import GameMode
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from httpx import AsyncClient
import httpx

from aiogram import F

router = Router()

@router.message(F.text, GameMode.waiting_for_answer)
async def test_word(message: Message, state: FSMContext):
    data = await state.get_data()
    correct_translate = data["translate"]
    if message.text != correct_translate:
        async with AsyncClient() as client:
            r: httpx.Response = await client.post(f'http://127.0.0.1:8000/game/{message.from_user.id}/{data["id"]}')
        await message.answer("Неприавльно, правильный перевод: " + correct_translate)
    else:
        await message.answer("Correct!")

    await state.clear()

    user_id = str(message.from_user.id)
    async with AsyncClient() as client:
        r: httpx.Response = await client.get(url=f'http://127.0.0.1:8000/game/{user_id}')
    if r.is_error:
        async with AsyncClient() as client:
            r_2: httpx.Response = await client.get(url=f'http://127.0.0.1:8000/game/wrong/{user_id}')
        response = ""
        for word in r_2.json():
            response += word["body"] + "\n"
        await message.answer("Слова закончились :)\nСписок неправильно переведённых слов: \n" + response)
        
        await message.answer("Введите /play чтобы начать с начала.\nИли /help чтобы узнать список комманд.")
        await state.clear()
    else:
        response = r.json()
        await state.update_data(response)
        await message.answer("Переведите слово: " + response["body"])
        await state.set_state(GameMode.waiting_for_answer)


