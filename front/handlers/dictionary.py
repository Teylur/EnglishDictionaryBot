from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
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
async def word_accepted(message: Message, state: FSMContext):
    word = await state.get_data()
    word = word["word"]
    await message.answer(word + " было добавлено в словарь!",)


@router.message(Dictionary.word)
@router.callback_query(lambda c: c.data == "word_reject")
async def word_accepted(message: Message, state: FSMContext, callback: CallbackQuery):
    word = await state.get_data()
    word = word["word"]
    await callback.answer()
    await callback.message.edit_caption("Слово " + word + " не было добавлено!", reply_markup=None)
    await state.clear()
    await message.answer("Не добавлено в словарь!",)



