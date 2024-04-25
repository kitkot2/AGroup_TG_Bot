import re
import csv
import numpy as np
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
import pandas as pd
from create_bot import CSV_FILENAME, all_users_data
from handlers.keyboard import make_row_keyboard

"""Регистрация"""

# Определение состояний пользователя с использованием StatesGroup
class User(StatesGroup):
    name = State()
    already_in_list = State()
    type_of_user = State()
    student_class = State()
    teacher_class = State()
 

# Обработчик команды /register
async def command_register(message: Message):
    all_users_data = pd.read_csv(CSV_FILENAME, sep=",", encoding = 'utf8') ######
    if message.from_user.id in np.array(all_users_data['ID']):
        my_string = all_users_data[all_users_data['ID'] == message.from_user.id]
        await User.already_in_list.set()
        await message.reply(
            text=f"Здравствуйте!\nВы уже зарегистрированы как {np.array(my_string['TYPE'])[-1]} {np.array(my_string['NAME'])[-1]} из класса {np.array(my_string['CLASS'])[-1]}.\nХотите изменить свои данные?",
            reply_markup=make_row_keyboard(["Да", "Нет"]),
        )
    else:
        await User.name.set()
        await message.reply(text = "Представьтесь пожалуйста!", reply_markup = ReplyKeyboardRemove())
        
# ID уже есть в файле, перезаписать?       
async def already_in_list_handler(message : Message, state: FSMContext, all_users_data=all_users_data):
    async with state.proxy() as data:
        data["already_in_list"] = message.text.lower()
    if data["already_in_list"].lower() == 'да':
        all_users_data = all_users_data.drop(all_users_data[all_users_data['ID'] == message.from_user.id].index[-1])
        all_users_data.reset_index(drop=True, inplace=True)
        all_users_data.to_csv(CSV_FILENAME, encoding = 'utf8', index=False)
        await User.name.set()
        await message.reply(text="Представьтесь пожалуйста!", 
                            reply_markup = ReplyKeyboardRemove(),)
    else:
        await state.finish()
        await message.reply(
            text="Действие отменено",
            reply_markup = ReplyKeyboardRemove(),
                            )
        

# Обработчик для ввода имени пользователя
async def intro_name(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    

    try:
        assert not re.search(r"[^а-яё ]", data["name"].lower())
        for word in data["name"].split(' '):
            assert len(word) > 1
            
        # Приведение имени в красивый вид
        
        name = ''

        for word in data["name"].split(' '):
            name += word[0].upper()
            name += word[1:].lower()
            if word in data["name"].split(' ')[:-1]:
                name += ' '
        
        async with state.proxy() as data:
            data["name"] = name

    except:
        await message.reply("Укажите своё имя корректно.")
    else:
        await User.type_of_user.set()
        await message.reply(
            text="Здравствуйте! Теперь укажите ваш статус учитель/ученик.",
            reply_markup=make_row_keyboard(["Учитель", "Ученик"]),
        )


# Обработчик для выбора типа пользователя (учитель/ученик)

async def type_of_user(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["type_of_user"] = message.text.lower()

    if data["type_of_user"].lower() == "учитель":
        await User.teacher_class.set()
        await message.reply(
            text="Через пробел введите названия классов, в которых вы преподаёте.",
            reply_markup=ReplyKeyboardRemove(),
        )
    elif data["type_of_user"].lower() == "ученик":
        await User.student_class.set()
        await message.reply(
            text="Введите класс, в котором вы учитесь.",
            reply_markup=ReplyKeyboardRemove(),
        )
    else:
        await message.reply(
            "Некорректный тип пользователя. Пожалуйста, выберите 'учитель' или 'ученик'."
        )


# Обработчик для ввода классов учителя
async def teacher_class_handler(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["teacher_class"] = message.text

    # Проверяем корректность названий классов
    for class_name in data["teacher_class"].split(" "):
        try:
            assert int(class_name[:-1]) <= 11
            assert int(class_name[:-1]) >= 1
            assert not re.search(r"[^а-яё]", class_name[-1].lower())
        except:
            await message.reply("Введите названия классов корректно.")
            break
        else:
            # Пишем данные в конец CSV файла
            if class_name == data["teacher_class"].split(" ")[-1]:
                with open(CSV_FILENAME, mode="a", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow(
                        [
                            message.from_user.id,
                            data["name"],
                            data["type_of_user"].lower(),
                            data["teacher_class"].upper(),
                        ]
                    )
                    print('Регистрация пользователя:', message.from_user.id,
                    data["name"],
                    data["type_of_user"].lower(),
                    data["teacher_class"].upper())
                await state.finish()
                await message.reply("Данные сохранены.")


# Обработчик для ввода класса ученика
async def student_class_handler(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data["student_class"] = message.text


    # Проверяем корректность названия класса
    try:
        int(data["student_class"][:-1])
        assert int(data["student_class"][:-1]) <= 11
        assert int(data["student_class"][:-1]) >= 1
        assert not re.search(r"[^а-яё]", data["student_class"][-1].lower())
        assert len(data["student_class"]) <= 3
    except:
        await message.reply("Введите название класса корректно.")
    else:
        # Пишем данные в конец CSV файла
        with open(CSV_FILENAME, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    message.from_user.id,
                    data["name"],
                    data["type_of_user"].lower(),
                    data["student_class"].upper(),
                ]
            )
            print('Регистрация пользователя:', message.from_user.id,
                    data["name"],
                    data["type_of_user"].lower(),
                    data["student_class"].upper())
        await state.finish()
        await message.reply("Данные сохранены")
        

def register_handlers_registration(dp : Dispatcher):
    dp.register_message_handler(command_register, commands=['register'])
    dp.register_message_handler(already_in_list_handler, state=User.already_in_list)
    dp.register_message_handler(intro_name, state=User.name)
    dp.register_message_handler(type_of_user, state=User.type_of_user)
    dp.register_message_handler(teacher_class_handler, state=User.teacher_class)
    dp.register_message_handler(student_class_handler, state=User.student_class)