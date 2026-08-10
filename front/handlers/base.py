from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from front.states.states import Dictionary, GameMode
from front.keyboards.dict_keyboards import get_dict_main_Readline_keyboard

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
async def help(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(GameMode.waiting_for_answer)
    await message.answer("Играть")

