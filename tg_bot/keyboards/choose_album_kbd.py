from aiogram import Dispatcher, types
from tg_bot.misc.albums_manage import get_albums


async def choose_album_btns(user_id):
    albums = await get_albums(user_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.add('В главное меню')
    keyboard.add('Добавить викторину')
    keyboard.add(*[f'{k} - {v}' for k, v in albums.items()])
    return keyboard
