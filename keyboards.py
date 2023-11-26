import os

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


dirs = os.listdir('materials')
list_dir = []
for folder in dirs:
    list_dir.append([InlineKeyboardButton(text=folder, callback_data=folder)])


kb_folders = InlineKeyboardMarkup(row_width=1, inline_keyboard=list_dir)
