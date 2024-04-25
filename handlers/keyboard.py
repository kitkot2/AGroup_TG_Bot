from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from aiogram.dispatcher import Dispatcher


# Функция для создания клавиатуры
def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)


def register_handlers_keyboard(dp : Dispatcher):
    dp.register_message_handler(make_row_keyboard)
