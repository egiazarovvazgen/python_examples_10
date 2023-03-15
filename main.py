from handlers import dsp
from aiogram.utils import executor


async def start_bot(_):
    print("Бот запущен")


if __name__ == "__main__":
    executor.start_polling(dsp, skip_updates=True, on_startup=start_bot)
