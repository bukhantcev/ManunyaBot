import os

from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from keyboards import kb_folders
from aiogram.types import InputFile





@dp.message_handler(commands=['go'])
async def go(message: Message):
    await message.answer(text='Выбери спектакль:', reply_markup=kb_folders)


@dp.callback_query_handler()
async def get_file(cb: CallbackQuery):
    try:
        name = cb.data
        for folder in os.listdir('materials'):
            if folder == name:
                for file in os.listdir(f'materials/{folder}'):
                    file_input = InputFile(f'materials/{folder}/{file}')
                    await bot.send_document(chat_id=cb.message.chat.id, document=file_input)
        


    except:
        await cb.answer(text="Залупу!")
