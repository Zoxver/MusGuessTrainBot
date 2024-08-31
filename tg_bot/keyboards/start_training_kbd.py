from aiogram import Dispatcher, types


async def start_training_btns():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add("Получить отрывок")
    keyboard.add("В главное меню")
    return keyboard
