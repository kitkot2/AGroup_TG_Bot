from create_bot import dp
from handlers import registration, cancel, keyboard, echo, show, sender, start

cancel.register_handlers_cancel(dp)
start.register_handlers_start(dp)
registration.register_handlers_registration(dp)
show.register_handlers_show(dp)
sender.register_handlers_sender(dp)
echo.register_handlers_echo(dp)
keyboard.register_handlers_keyboard(dp)

# Функция, которая выполняется при запуске бота
async def on_startup(_):
    print("Бот онлайн")

    # Штука для того чтобы бот не обрабатывал сообщения после выхода из оффлайн режима
if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)