from aiogram.types import (
    Message,
)
from handlers.keyboard import make_row_keyboard
from aiogram.dispatcher import Dispatcher, FSMContext
import numpy as np
from create_bot import all_users_data, CSV_FILENAME
import pandas as pd


async def command_start(message: Message, state:FSMContext):
    all_users_data = pd.read_csv(CSV_FILENAME, sep=",", encoding = 'utf8') ######
    if message.from_user.id not in np.array(all_users_data['ID']):
        
        await message.reply(
            text= 'Зарегистрируйтесь, пожалуйста.',
            reply_markup=make_row_keyboard(["/register"]),
        )
    elif message.from_user.id in np.array(all_users_data['ID']):
        my_string = all_users_data[all_users_data['ID'] == message.from_user.id]
        my_string.reset_index()
        my_string = my_string.loc[my_string.index[-1]]
        if my_string['TYPE'] == 'учитель':
            await message.reply(
                text=f"Здравствуйте, {my_string['NAME']}!",
                reply_markup=make_row_keyboard(["/register", "/show", "/send", "/cancel"]),
            )
        elif my_string['TYPE'] == 'ученик':
            await message.reply(
                text=f"Здравствуйте, {my_string['NAME']}!",
                reply_markup=make_row_keyboard(["/register", "/cancel"]),
            )

def register_handlers_start(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])