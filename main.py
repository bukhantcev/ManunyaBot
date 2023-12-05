import os
from loader import dp
from aiogram.utils import executor
from handlers import dp
from db_config import create_table



async def on_start(_):
    create_table()
    print('Bot run')







executor.start_polling(dp, skip_updates=True, on_startup=on_start)

