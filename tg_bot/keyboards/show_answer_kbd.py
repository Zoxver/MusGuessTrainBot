from aiogram import Dispatcher, types


async def show_answer_btns():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text='Показать ответ', callback_data='show_answer')
    keyboard.add(button)
    return keyboard
