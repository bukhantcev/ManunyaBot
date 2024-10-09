import os

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

memory = MemoryStorage()


bot = Bot(os.getenv('TOKEN'))
# bot = Bot('6283280993:AAHi8EqmQ41zE8rLl_0ayUexaX69DlCxs20')

dp = Dispatcher(bot, storage=memory)