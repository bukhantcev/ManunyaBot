from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from loader import dp
from aiogram.types import Message, CallbackQuery


class NewItem(StatesGroup):
    citi = State()
    sklad = State()
    sklad_vidacha = State()
    sklad_delete = State()
    translated_sl = State()
    translated_dl = State()
    translated_text = State()

