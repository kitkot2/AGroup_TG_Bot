from aiogram import Bot
from aiogram import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import pandas as pd

storage = MemoryStorage()

# Имя файла, в который будут сохраняться данные
CSV_FILENAME = "all_users_data.csv"

# Наша табличка
all_users_data = pd.read_csv(CSV_FILENAME, sep=",", encoding = 'utf8')
with open('token.txt', 'r') as file:
    token = file.read().strip()
bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)