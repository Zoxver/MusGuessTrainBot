from aiogram import Dispatcher, types


async def menu_btns():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add('Начать тренировку')
    keyboard.add('Мои викторины')
    return keyboard
