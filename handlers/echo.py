from aiogram.types import (
Message,
)
from aiogram.dispatcher import Dispatcher
from create_bot import bot


# Обработчик неизвестных сообщений
async def echo_send(message: Message):
    await bot.send_message(
        message.from_user.id,
        text=f"Неизвестная команда.\nДля начала работы введите /start\n",
    )


def register_handlers_echo(dp : Dispatcher):
    dp.register_message_handler(echo_send)