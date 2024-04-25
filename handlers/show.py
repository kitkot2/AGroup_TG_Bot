import numpy as np
import pandas as pd
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from create_bot import all_users_data, CSV_FILENAME
from handlers.keyboard import make_row_keyboard


class Show_class(StatesGroup):
    ready_to_write_class = State()
    ready_to_write = State()



async def start_show(message: Message, state: FSMContext):
    all_users_data = pd.read_csv(CSV_FILENAME, sep=",", encoding = 'utf8') ######
    my_string = all_users_data.loc[all_users_data[all_users_data["ID"] == message.from_user.id].index[-1]]

    if my_string["TYPE"] == "учитель":
        await Show_class.ready_to_write_class.set()
        async with state.proxy() as data:
            data["teacher_name"] = my_string["NAME"]
        await message.reply(
            text="Введите название класса, список зарегистрированных участников которого вы хотите посмотреть:",
            reply_markup=make_row_keyboard(my_string["CLASS"].split(" ")),
        )
    else:
        await state.finish()
        await message.reply("Вы не учитель.")


async def show_what_class(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["show_class"] = message.text
    try:
        student_data = all_users_data[all_users_data["TYPE"] == 'ученик']
        show_str = student_data[student_data["CLASS"] == data["show_class"]].set_index('NAME').sort_index().index
        show_message = ''
        for i in range(len(show_str)):
            show_message += f'{i+1}. {show_str[i]}\n'
        await state.finish()

        await message.reply(
            text= show_message,
            reply_markup=ReplyKeyboardRemove(),
        )
    except:
        await state.finish()
        await message.reply(
            text='В этом классе пока никто не зарегистрировался.',
            reply_markup=ReplyKeyboardRemove(),
        )


def register_handlers_show(dp : Dispatcher):
    dp.register_message_handler(start_show, commands=['show'], state=None)
    dp.register_message_handler(show_what_class, state=Show_class.ready_to_write_class)
