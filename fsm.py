from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import dp
from aiogram.types import Message, CallbackQuery


class NewItem(StatesGroup):
    citi = State()

