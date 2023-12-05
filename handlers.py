import os

from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from keyboards import kb_folders, kb_vidacha
from aiogram.types import InputFile
from pogoda import get_pogoda
from fsm import NewItem
from aiogram.dispatcher import FSMContext
from db_config import add_new_worker, get_list, update_list





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
        await message.answer('Где, бля?')
        await NewItem.citi.set()

    if message.text.lower() == 'сохрани':
        await message.answer('Присылай, сохраню, хули!')
        await NewItem.sklad.set()

    if message.text.lower() == 'выдай базу':
        await message.answer('Выбирай, ёпта!', reply_markup=kb_vidacha)
        await NewItem.sklad_vidacha.set()





    tg_id = message.from_user.id
    list_docs = ''
    new_worker = (tg_id, list_docs)
    add_new_worker(new_worker=new_worker)

@dp.message_handler(state=NewItem.citi)
async def send_pogoda(message:Message, state:FSMContext):
    try:
        await message.answer(text=get_pogoda(message.text))
    except:
        await message.answer("В душе не ебу где это!!! Нормально напиши!")
    await state.finish()


@dp.message_handler(content_types=['photo', 'video', 'document', 'audio', 'voice'], state=NewItem.sklad)
async def prinyat_na_sklad(message:Message, state: FSMContext):
    old_list = ''
    info = ''
    if 'photo' in message:
        info = message.photo[-1].file_id
        column = 'list_photo'
        old_list = get_list((message.from_user.id,), column=column)[0][0]

    if 'document' in message:
        info = message.document.file_id
        column = 'list_docs'
        old_list = get_list((message.from_user.id,), column=column)[0][0]

    if 'video' in message:
        info = message.video.file_id
        column = 'list_video'
        old_list = get_list((message.from_user.id,), column=column)[0][0]

    if 'audio' in message:
        info = message.audio.file_id
        column = 'list_audio'
        old_list = get_list((message.from_user.id,), column=column)[0][0]

    if 'voice' in message:
        info = message.voice.file_id
        column = 'list_voice'
        old_list = get_list((message.from_user.id,), column=column)[0][0]


    if old_list == None or old_list == '':
        new_list = info
    else:
        new_list = f'{old_list}, {info}'
    tg_id = message.from_user.id
    new_data = (new_list, tg_id)
    update_list(new_data=new_data, column=column)
    await message.answer('Сохранил! С тебя 🥃')
    await state.finish()


@dp.callback_query_handler(state=NewItem.sklad_vidacha)
async def vidacha(cb:CallbackQuery, state:FSMContext):

    column = ''
    if cb.data == 'photo':
        column = 'list_photo'
        if get_list(tg_id=(cb.from_user.id,), column=column) != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column) != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_photo(chat_id=cb.message.chat.id, photo=id, caption=id)
            await state.finish()
        else:
            await cb.answer('Нет ни хуя тут!!!')
            await state.finish()
    if cb.data == 'video':
        column = 'list_video'
        if get_list(tg_id=(cb.from_user.id,), column=column) != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column) != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_video(chat_id=cb.message.chat.id, video=id, caption=id)
            await state.finish()
        else:
            await cb.answer('Нет ни хуя тут!!!')
            await state.finish()
    if cb.data == 'document':
        column = 'list_docs'
        if get_list(tg_id=(cb.from_user.id,), column=column) != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column) != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_document(chat_id=cb.message.chat.id, document=id, caption=id)
            await state.finish()
        else:
            await cb.answer('Нет ни хуя тут!!!')
            await state.finish()
    if cb.data == 'audio':
        column = 'list_audio'
        if get_list(tg_id=(cb.from_user.id,), column=column) != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column) != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_audio(chat_id=cb.message.chat.id, audio=id, caption=id)
            await state.finish()
        else:
            await cb.answer('Нет ни хуя тут!!!')
            await state.finish()
    if cb.data == 'voice':
        column = 'list_voice'
        if get_list(tg_id=(cb.from_user.id,), column=column) != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column) != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_voice(chat_id=cb.message.chat.id, voice=id, caption=id)
            await state.finish()
        else:
            await cb.answer('Нет ни хуя тут!!!')
            await state.finish()









