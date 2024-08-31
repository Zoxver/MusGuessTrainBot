from aiogram import Dispatcher, types


async def share_album_btns():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Да, поделиться')
    keyboard.add('Нет, вернуться назад')
    return keyboard
