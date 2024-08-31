import logging
import random
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from tg_bot.keyboards.choose_album_kbd import choose_album_btns
from tg_bot.keyboards.menu_kbd import menu_btns
from tg_bot.keyboards.show_answer_kbd import show_answer_btns
from tg_bot.keyboards.start_training_kbd import start_training_btns
from tg_bot.keyboards.training_kbd import training_btns
from tg_bot.misc.albums_manage import get_albums, delete_album
from tg_bot.misc.tracks_manage import get_tracks, tracks_count, add_track, delete_track, get_track_fragment, \
    delete_track_fragment


class ChooseAction(StatesGroup):
    pick_album = State()
    training = State()


async def bot_training(message: types.Message, state: FSMContext):
    data = await state.get_data()
    album_id = data.get('album_id')
    tracks = data.get('tracks')
    user_id = message.from_user.id
    if message.text in ('Получить отрывок', 'Следующий отрывок'):
        track_name = random.choice(list(tracks.keys()))
        track_name_mp3 = tracks[track_name]
        track = await get_track_fragment(user_id, album_id, track_name_mp3)
        await state.update_data(data={'track_name': track_name})
        await message.answer_audio(types.InputFile(f"music_data/{user_id}/{album_id}/{track}"),
                                   reply_markup=await show_answer_btns())
        await delete_track_fragment(user_id, album_id, track)
    elif message.text == 'В главное меню':
        await message.answer("Выберите действие", reply_markup=await menu_btns())
        await state.finish()
    else:
        await message.answer("Неизвестная команда", reply_markup=await training_btns())
        return


async def bot_pick_album(message: types.Message, state: FSMContext):
    album_id = message.text.split()[0]
    tracks = await get_tracks(message.from_user.id, album_id)
    if not tracks:
        await message.answer("Эта викторина пуста", reply_markup=await menu_btns())
        await state.finish()
        return
    await state.update_data(data={'album_id': album_id, 'tracks': tracks})
    await message.answer(f"Выбрана викторина {' '.join(message.text.split()[2:])}",
                         reply_markup=await start_training_btns())
    await state.set_state(ChooseAction.training.state)


async def bot_show_answer(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    track_name = data["track_name"]
    await callback_query.message.edit_caption(f"Ответ: {track_name}")


async def bot_start_training(message: types.Message, state: FSMContext):
    await state.set_state(ChooseAction.pick_album.state)
    await message.answer(f"Выберите викторину для тренировки",
                         reply_markup=await choose_album_btns(message.from_user.id))


def register_start_training(dp: Dispatcher):
    dp.register_message_handler(bot_start_training, Text(equals=['Начать тренировку', '/start_training']),
                                state='*')
    dp.register_message_handler(bot_pick_album, regexp="^[1-9][0-9]* - .+$", state=ChooseAction.pick_album)
    dp.register_message_handler(bot_training, content_types=types.ContentType.TEXT, state=ChooseAction.training)
    dp.register_callback_query_handler(bot_show_answer, state=ChooseAction.training)
