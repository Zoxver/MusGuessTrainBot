from aiogram import Dispatcher, types


async def manage_album_btns():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add("Список файлов")
    keyboard.add("Добавить файл")
    keyboard.add("Удалить викторину")
    keyboard.add("Поделиться викториной")
    keyboard.add("Мои викторины")
    keyboard.add("В главное меню")
    return keyboard
