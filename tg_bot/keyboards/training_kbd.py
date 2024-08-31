from aiogram import Dispatcher, types


async def training_btns():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add("Следующий отрывок")
    keyboard.add("В главное меню")
    return keyboard
