import logging
from aiogram import Dispatcher, types
from tg_bot.keyboards.choose_album_kbd import choose_album_btns
from aiogram.dispatcher.filters import Text
from tg_bot.misc.albums_manage import get_albums


async def bot_albums(message: types.Message):
    albums = await get_albums(message.from_user.id)
    if not albums:
        await message.answer("У вас еще нет ни одной викторины.\nНажмите кнопку ниже для добавления викторины.",
                             reply_markup=await choose_album_btns(message.from_user.id))
    else:
        await message.answer("Выберите викторину или добавьте новую",
                             reply_markup=await choose_album_btns(message.from_user.id))


def register_albums(dp: Dispatcher):
    dp.register_message_handler(bot_albums, Text(equals=['Мои викторины', '/albums']))
