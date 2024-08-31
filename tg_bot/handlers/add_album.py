import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from tg_bot.keyboards.choose_album_kbd import choose_album_btns
from aiogram.dispatcher.filters import Text, Command
from tg_bot.misc.albums_manage import albums_count, add_album


class AlbumStates(StatesGroup):
    getting_album_name = State()


async def bot_add_album(message: types.Message, state: FSMContext):
    if await albums_count(message.from_user.id) >= 32:
        await message.answer("Извините, вы не можете добавлять больше 32 викторин", reply_markup=await choose_album_btns(message.from_user.id))
        return
    await message.answer("Введите название викторины", reply_markup=await choose_album_btns(message.from_user.id))
    await state.set_state(AlbumStates.getting_album_name.state)


async def bot_get_album_name(message: types.Message, state: FSMContext):
    if len(message.text) > 100:
        await message.answer("Название не может быть больше 100 символов", reply_markup=await choose_album_btns(message.from_user.id))
        return
    album_name = message.text.replace('\n', ' ')
    await add_album(message.from_user.id, album_name)
    await message.answer("Викторина была добавлена", reply_markup=await choose_album_btns(message.from_user.id))
    await state.finish()


def register_add_album(dp: Dispatcher):
    dp.register_message_handler(bot_add_album,
                                Text(equals=['Добавить викторину', '/add_album']), state='*')
    dp.register_message_handler(bot_get_album_name, state=AlbumStates.getting_album_name.state)
