import os

from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from keyboards import kb_folders
from aiogram.types import InputFile
from pogoda import get_pogoda
from fsm import NewItem
from aiogram.dispatcher import FSMContext





@dp.message_handler(commands=['go'])
async def go(message: Message):
    await message.answer(text='Выбери спектакль:', reply_markup=kb_folders)


@dp.callback_query_handler()
async def get_file(cb: CallbackQuery):
    try:
        await cb.answer('На, нахуй!!!')
        name = cb.data
        for folder in os.listdir('materials'):
            if folder == name:
                for file in os.listdir(f'materials/{folder}'):
                    file_input = InputFile(f'materials/{folder}/{file}')
                    await bot.send_document(chat_id=cb.message.chat.id, document=file_input)
        


    except:
        await cb.answer(text="Залупу!")


@dp.message_handler(state=None)
async def send_stickers(message:Message, state: FSMContext):
    if 'да' in message.text.lower() and 'конечно' in message.text.lower():
        sticker = InputFile('stickers/da_konechno.jpg')
        await message.answer_photo(photo=sticker)

    if 'это моя работа' in message.text.lower():
        sticker = InputFile('stickers/job.jpg')
        await message.answer_photo(photo=sticker)

    if 'бублик' in message.text.lower() or 'баблгам' in message.text.lower():
        sticker = InputFile('stickers/bublik.jpg')
        await message.answer_photo(photo=sticker)

    if message.text.lower() == 'погода':
        await NewItem.citi.set()

@dp.message_handler(state=NewItem.citi)
async def send_pogoda(state:FSMContext, message:Message):
    await message.answer(text=get_pogoda(message.text))
    await state.finish()



