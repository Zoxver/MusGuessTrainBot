import logging
from tg_bot.keyboards.menu_kbd import menu_btns
from tg_bot.keyboards.ready_kbd import ready_btns
from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from tg_bot.misc.albums_manage import add_public_album


async def bot_start_with_params(message: types.Message, state: FSMContext):
    params = message.get_args()
    from_user_id, album_id = params.split('_')
    msg = await add_public_album(message.from_user.id, from_user_id, album_id)
    await message.answer(msg, reply_markup=await menu_btns())
    await state.finish()


async def bot_start(message: types.Message, state: FSMContext):
    await message.answer("Привет! Это бот для тренировки\nГотов начать?",
                         reply_markup=await ready_btns())
    await state.finish()


def register_start(dp: Dispatcher):
    dp.register_message_handler(bot_start, Text(equals=['/start', 'Вернуться в начало']), state='*')
    dp.register_message_handler(bot_start_with_params, regexp="^/start [0-9]+_[1-9][0-9]*$", state='*')
