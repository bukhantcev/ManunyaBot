from loader import dp
from aiogram.types import Message, CallbackQuery
from keyboards import kb_folders




@dp.message_handler(commands=['go'])
async def go(message: Message):
    await message.answer(text='Выбери спектакль:', reply_markup=kb_folders)


@dp.callback_query_handler()
async def get_file(cb: CallbackQuery):
    try:
        name = cb.data
        


    except:
        pass
