from aiogram import Dispatcher, types


async def ready_btns():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Готов!')
    return keyboard