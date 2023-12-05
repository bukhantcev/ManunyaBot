import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


dirs = os.listdir('materials')
list_dir = []
for folder in dirs:
    list_dir.append([InlineKeyboardButton(text=folder, callback_data=folder)])


kb_folders = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_dir)

vidacha = [
    [InlineKeyboardButton(text='Фотки', callback_data='photo')],
    [InlineKeyboardButton(text='Видосы', callback_data='video')],
    [InlineKeyboardButton(text='Доки всякие', callback_data='document')],
    [InlineKeyboardButton(text='Музыка', callback_data='audio')],
    [InlineKeyboardButton(text='Голосовухи', callback_data='voice')]

]

kb_vidacha = InlineKeyboardMarkup(row_width=1, inline_keyboard=vidacha)
