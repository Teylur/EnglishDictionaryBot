from aiogram import Router
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from front.states.states import GameMode
from aiogram.fsm.context import FSMContext
from aiogram import F

router = Router()

@router.message(F.text, GameMode.waiting_for_answer)
async def game(message: Message):
    await message.answer("Game is started!")