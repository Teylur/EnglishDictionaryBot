from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           ReplyKeyboardMarkup, KeyboardButton)

def get_accept_reject_inline_keyboard() ->InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Добавить", callback_data="word_accept"),
           InlineKeyboardButton(text="Отклонить", callback_data="word_reject")]
           ]
    )
    return keyboard

def get_dict_main_Readline_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text="Список слов"), KeyboardButton(text="Играть")]
    ])
    return keyboard

def get_dict_delete_word_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Удалить слово", callback_data="word_delete")]
        ]
    )
    return keyboard
def get_dict_back_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Назад", callback_data="back")]
        ]
    )
    return keyboard