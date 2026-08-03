from aiogram.fsm.state import StatesGroup, State

class GameMode(StatesGroup):
    waiting_for_answer = State()

class Dictionary(StatesGroup):
    word = State()