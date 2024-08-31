from aiogram import Dispatcher, types


async def delete_track_btns():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Удалить файл', callback_data='delete_track')
    keyboard.add(button)
    return keyboard
