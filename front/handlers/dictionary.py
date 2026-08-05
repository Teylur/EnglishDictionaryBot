from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
import httpx
from front.states.states import GameMode, Dictionary
from aiogram.fsm.context import FSMContext
from aiogram import F

router = Router()

def get_accept_reject_inline_keyboard() ->InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить", callback_data="word_accept"),
           InlineKeyboardButton(text="Отклонить", callback_data="word_reject")]
           ]
    )
    return keyboard

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
    r: httpx.Response = httpx.post('http://127.0.0.1:8000/dict', json={'id': '1', 'body': word})
    await callback.message.edit_text(word + " было добавлено в словарь! ✔",)


@router.message(Dictionary.word)
@router.callback_query(lambda c: c.data == "word_reject")
async def word_accepted(callback: CallbackQuery, state: FSMContext):
    word = await state.get_data()
    word = word["word"]
    await state.clear()
    await callback.message.edit_text(f"Слово {word} не добавлено в словарь! ❌", reply_markup=None)
    await state.set_state(Dictionary.word)





