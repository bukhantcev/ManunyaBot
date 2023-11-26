import os
from loader import dp
from aiogram.utils import executor
from handlers import dp



async def on_start(_):
    print('Bot run')







executor.start_polling(dp, skip_updates=True, on_startup=on_start)

