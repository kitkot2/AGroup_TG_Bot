from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

# Сброс машины состояния
async def cancel_handler(message: Message, state: FSMContext):
    await message.answer(
        text="Действие отменено", 
        reply_markup=ReplyKeyboardRemove(),
        )
    await state.finish()

def register_handlers_cancel(dp : Dispatcher):
    dp.register_message_handler(cancel_handler, commands = ['cancel'], state = '*')