
import numpy as np
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from create_bot import bot, all_users_data, CSV_FILENAME
from handlers.keyboard import make_row_keyboard
import pandas as pd


class Send_from_teacher(StatesGroup):
    ready_to_write_class = State()
    ready_to_write = State()
    ready_to_send = State()
    
# Функция для создания клавиатуры
def make_row_keyboard(items: list[str]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)



async def start_send(message: Message, state: FSMContext):
    all_users_data = pd.read_csv(CSV_FILENAME, sep=",", encoding = 'utf8') ######
    global my_string
    my_string = all_users_data[all_users_data["ID"] == message.from_user.id]
    my_string.reset_index(drop=True, inplace=True)

    if my_string["TYPE"][0] == "учитель":
        await Send_from_teacher.ready_to_write_class.set()
        async with state.proxy() as data:
            data["teacher_name"] = my_string["NAME"][0]
        await message.reply(
            text="Введите название класса, которому вы хотите написать:",
            reply_markup=make_row_keyboard(my_string["CLASS"][0].split(" ")),
        )
    else:
        await state.finish()
        await message.reply("Вы не учитель.")


async def send_what_class(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["send_class"] = message.text
    await Send_from_teacher.ready_to_write.set()
    await message.reply(
        text="Напишите сообщение, которое вы хотите отправить",
        reply_markup=ReplyKeyboardRemove(),
    )


async def send_from_teacher(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["teacher_message"] = message.text

    await Send_from_teacher.ready_to_send.set()
    await message.reply(
        text=f"Вы точно хотите отправить это сообщение классу {data['send_class']}?\n\nОт: {data['teacher_name']}\n{data['teacher_message']}",
        reply_markup=make_row_keyboard(["Да", "Нет"]),
    )


async def send_ready(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["yes"] = message.text
    if data["yes"].lower() == "да":
        for student_id in np.array(
            all_users_data[all_users_data["CLASS"] == data["send_class"]]["ID"]
        ):
            if student_id != message.from_user.id:
                await bot.send_message(
                    student_id,
                    text=f"От: {data['teacher_name']}\n{data['teacher_message']}",
                )
            
        await message.reply(
            text="Сообщения отправлены.", reply_markup=ReplyKeyboardRemove()
        )
        print(f"Учитель {my_string['NAME']} отправил сообщение \'{data['teacher_message']}\' классу {data['send_class']}")
    else:
        await message.reply(
            text="Сообщения не отправлены.", reply_markup=ReplyKeyboardRemove()
        )
    await state.finish()
    

def register_handlers_sender(dp : Dispatcher):
    dp.register_message_handler(start_send, commands=['send'])
    dp.register_message_handler(send_what_class, state=Send_from_teacher.ready_to_write_class)
    dp.register_message_handler(send_from_teacher, state=Send_from_teacher.ready_to_write)
    dp.register_message_handler(send_ready, state=Send_from_teacher.ready_to_send)
    