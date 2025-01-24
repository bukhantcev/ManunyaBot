import os
import random

from loader import dp, bot
from aiogram.types import Message, CallbackQuery
from keyboards import kb_folders, kb_vidacha, kb_translated
from aiogram.types import InputFile
from pogoda import get_pogoda
from fsm import NewItem
from aiogram.dispatcher import FSMContext
from db_config import add_new_worker, get_list, update_list
import asyncio
from translated import get_translator
from manual import text_help
import requests
from dip import set_dip_switches





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

    if message.text.lower() == 'погода':
        await message.answer('Где, бля?')
        await NewItem.citi.set()

    if message.text.lower() == 'сохрани':
        await message.answer('Присылай, сохраню, хули!')
        await NewItem.sklad.set()

    if message.text.lower() == 'выдай базу':
        await message.answer('Ты подергай, а я посмотрю!', reply_markup=kb_vidacha)
        await NewItem.sklad_vidacha.set()

    if message.text.lower() == 'удали':
        await message.answer('Скопируй и пришли мне название!', reply_markup=None)
        await NewItem.sklad_delete.set()

    if message.text.lower() == 'переведи':
        await message.answer('Что-куда?', reply_markup=kb_translated)
        await NewItem.translated_sl.set()

    if 'help' in message.text.lower():
        await message.answer(text=text_help)


    if message.text.lower() == 'чч':
        url_text = 'http://api.forismatic.com/api/1.0/'
        data = {'method': 'getQuote', 'format': 'text', 'lang': 'ru'}
        citata = requests.post(url_text, data=data).text
        await message.answer(citata)

    if message.text.lower() == 'dip' or message.text.lower() == 'дип':
        await message.answer('Пришли адрес!')
        await NewItem.dip_switch.set()



    tg_id = message.from_user.id
    list_docs = None
    new_worker = (tg_id, list_docs)
    add_new_worker(new_worker=new_worker)

@dp.message_handler(state=NewItem.citi)
async def send_pogoda(message:Message, state:FSMContext):
    try:
        await message.answer(text=get_pogoda(message.text))
    except:
        await message.answer("В душе не ебу где это!!! Нормально напиши!")
    await state.finish()

@dp.message_handler(state=NewItem.dip_switch)
async def send_dip(message:Message, state:FSMContext):
    if str(message.text).isdigit():
        if int(message.text) <= 512:
            try:
                await message.answer(text=set_dip_switches(message.text))
            except:
                await message.answer("Нужно ввести корректный адрес")
            await state.finish()
        else:
            await message.answer("Адрес не может быть больше 512")
            await state.finish()
    else:
        await message.answer("Адрес должен состоять только из цифр")
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
        if get_list(tg_id=(cb.from_user.id,), column=column)[0][0] != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column)[0][0] != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_photo(chat_id=cb.message.chat.id, photo=id, caption=id)
        else:
            await cb.answer('Нет ни хуя тут!!!')
    if cb.data == 'video':
        column = 'list_video'
        if get_list(tg_id=(cb.from_user.id,), column=column)[0][0] != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column)[0][0] != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_video(chat_id=cb.message.chat.id, video=id, caption=id)
        else:
            await cb.answer('Нет тут ни хуя!!!')
    if cb.data == 'document':
        column = 'list_docs'
        if get_list(tg_id=(cb.from_user.id,), column=column)[0][0] != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column)[0][0] != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_document(chat_id=cb.message.chat.id, document=id, caption=id)
        else:
            await cb.answer('Пусто!!!')
    if cb.data == 'audio':
        column = 'list_audio'
        if get_list(tg_id=(cb.from_user.id,), column=column)[0][0] != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column)[0][0] != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_audio(chat_id=cb.message.chat.id, audio=id, caption=id)
        else:
            await cb.answer('Тут зиро, ноль, пусто!!!')
    if cb.data == 'voice':
        column = 'list_voice'
        if get_list(tg_id=(cb.from_user.id,), column=column)[0][0] != None and get_list(tg_id=(cb.from_user.id,),
                                                                                  column=column)[0][0] != '':
            await cb.answer('На, нахуй!!!')
            ids = str(get_list(tg_id=(cb.from_user.id,), column=column)[0][0]).split(', ')
            for id in ids:
                await bot.send_voice(chat_id=cb.message.chat.id, voice=id, caption=id)
        else:
            await cb.answer('Ты заебал!!!')

    if cb.data == 'exit':
        await cb.answer('На, нахуй!!!')
        await bot.send_message(chat_id=cb.message.chat.id, text="Пока!")
        await bot.delete_message(chat_id=cb.message.chat.id, message_id=cb.message.message_id)
        await state.finish()
    await asyncio.sleep(120)
    try:
        await bot.delete_message(chat_id=cb.message.chat.id, message_id=cb.message.message_id)
        await state.finish()
    except:
        pass


@dp.message_handler(state=NewItem.sklad_delete)
async def sklad_delete(message:Message, state:FSMContext):
    list_column = ['list_photo', 'list_docs', 'list_video', 'list_audio', 'list_voice']
    for column in list_column:
        list_type = str(get_list(tg_id=(message.from_user.id,), column=column)[0][0]).split(', ')
        for id in list_type:
            if message.text == id:
                list_type.remove(id)
                new_string = ', '.join(list_type)
                new_data = (new_string, message.from_user.id)
                update_list(new_data=new_data, column=column)
    await message.answer('Удалил))')
    await state.finish()



@dp.callback_query_handler(state=NewItem.translated_sl)
async def get_sl(cb:CallbackQuery, state:FSMContext):
    data = cb.data
    await state.update_data({'translated_sl':data})
    await cb.answer('Куда?')
    await NewItem.translated_dl.set()

@dp.callback_query_handler(state=NewItem.translated_dl)
async def get_dl(cb:CallbackQuery, state:FSMContext):
    data = cb.data
    await state.update_data({'translated_dl':data})
    await cb.answer('Отправь текст!')
    await NewItem.translated_text.set()

@dp.message_handler(state=NewItem.translated_text)
async def get_text(message:Message, state:FSMContext):
    sl = await state.get_data()
    dl = await state.get_data()
    sl = sl.get('translated_sl')
    dl = str(dl.get('translated_dl')).split('_')[0]
    text = message.text
    await message.answer(text=get_translator(sl, dl, text))
    await state.finish()


@dp.message_handler(state='*')
async def exit_all(message:Message, state:FSMContext):
    if message.text.lower() == 'выход':
        await state.finish()
        await message.answer('Пока')













