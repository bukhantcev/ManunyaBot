import os

from aiogram import Bot, Dispatcher


bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher(bot)