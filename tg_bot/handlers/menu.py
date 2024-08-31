import logging
from tg_bot.keyboards.menu_kbd import menu_btns
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text

async def bot_menu(message: types.Message):
    await message.answer("Выберите действие", reply_markup=await menu_btns())


def register_menu(dp: Dispatcher):
    dp.register_message_handler(bot_menu, Text(equals=['Готов!', 'В главное меню', '/menu']))