from aiogram import Router
from aiogram.types import Message, CallbackQuery
import httpx
from httpx import AsyncClient as client
from front.states.states import GameMode, Dictionary
from aiogram.fsm.context import FSMContext
from aiogram import F
from front.keyboards.dict_keyboards import get_accept_reject_inline_keyboard, get_dict_main_Readline_keyboard

router = Router()

#word list
@router.message(Dictionary.word, F.text=="Список слов")
async def word_list(message: Message):
    r: httpx.Response = await client.get('http://127.0.0.1:8000/dict')
    response = "Dictionary:\n"
    for word in r.json():
        response += word["body"] + "\n"
    await message.answer(text=response)

#main state
@router.message(Dictionary.word, F.text)
async def dictionary(message: Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state == GameMode.waiting_for_answer:
        return
    await state.update_data(word=message.text)
    await message.answer(message.text, reply_markup=get_accept_reject_inline_keyboard())

@router.message(Dictionary.word)
@router.callback_query(lambda c: c.data == "word_accept")
async def word_accepted(callback: CallbackQuery, state: FSMContext):
    word = await state.get_data()
    word = word["word"]
    r: httpx.Response = client.post('http://127.0.0.1:8000/dict', json={'body': word})
    await callback.message.edit_text(word + " было добавлено в словарь! ✔",)


@router.message(Dictionary.word)
@router.callback_query(lambda c: c.data == "word_reject")
async def word_reject(callback: CallbackQuery, state: FSMContext):
    word = await state.get_data()
    word = word["word"]
    await state.clear()
    await callback.message.edit_text(f"Слово {word} не добавлено в словарь! ❌", reply_markup=None)
    await state.set_state(Dictionary.word)







