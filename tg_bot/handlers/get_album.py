import logging
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from tg_bot.keyboards.choose_album_kbd import choose_album_btns
from tg_bot.keyboards.delete_track_kbd import delete_track_btns
from tg_bot.keyboards.manage_album_kbd import manage_album_btns
from tg_bot.keyboards.menu_kbd import menu_btns
from tg_bot.keyboards.share_album_kbd import share_album_btns
from tg_bot.misc.albums_manage import get_albums, delete_album, album_make_public
from tg_bot.misc.tracks_manage import get_tracks, tracks_count, add_track, delete_track


class ChooseAction(StatesGroup):
    album = State()
    track_name = State()
    track = State()
    share_album = State()


async def bot_default_action_album(message: types.Message, state: FSMContext):
    if message.text == 'Мои викторины':
        albums = await get_albums(message.from_user.id)
        if not albums:
            await message.answer("У вас еще нет ни одной викторины.\nНажмите кнопку ниже для добавления викторины.",
                                 reply_markup=await choose_album_btns(message.from_user.id))
        else:
            await message.answer("Выберите викторину или добавьте новую",
                                 reply_markup=await choose_album_btns(message.from_user.id))
        await state.finish()
    elif message.text == 'В главное меню':
        await message.answer("Выберите действие", reply_markup=await menu_btns())
        await state.finish()


async def bot_action_album(message: types.Message, state: FSMContext):
    data = await state.get_data()
    album_id = data.get(f'album_id')
    if message.text == 'Список файлов':
        tracks = await get_tracks(message.from_user.id, album_id)
        if not tracks:
            await message.answer("Эта викторина пуста", reply_markup=await manage_album_btns())
            return
        for name, file in tracks.items():
            await message.answer_audio(types.InputFile(f"music_data/{message.from_user.id}/{album_id}/{file}"),
                                       caption=name, reply_markup=await delete_track_btns())
    elif message.text == 'Добавить файл':
        if await tracks_count(message.from_user.id, album_id) >= 100:
            await message.answer("В викторине может быть не более 100 файлов", reply_markup=await manage_album_btns())
            return
        await message.answer("Введите название файла")
        await state.set_state(ChooseAction.track_name.state)
    elif message.text == 'Удалить викторину':
        await delete_album(message.from_user.id, album_id)
        await message.answer("Викторина успешно удалена", reply_markup=await choose_album_btns(message.from_user.id))
        await state.finish()
    elif message.text == 'Поделиться викториной':
        await message.answer("Это действие сделает викторину доступной для любого пользователя.\n"
                             "Вы уверены, что вы хотите поделиться викториной?",
                             reply_markup=await share_album_btns())
        await state.set_state(ChooseAction.share_album.state)
    else:
        await message.answer("Неизвестная команда", reply_markup=await manage_album_btns())


async def bot_get_track_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    album_id = data.get('album_id')
    tracks = await get_tracks(message.from_user.id, album_id)
    if len(message.text) > 100:
        await message.answer("Слишком длинное название файла")
        return
    elif message.text in tracks.keys():
        await message.answer("Файл с таким именем уже есть, введите другое название")
        return
    else:
        await state.update_data(data={f'track_name': message.text})
        await message.answer("Пришлите аудио файл в формате mp3 размером до 2000мб")
        await state.set_state(ChooseAction.track.state)


async def bot_get_track(message: types.Message, state: FSMContext):
    if message.audio.file_name.split(".")[-1] != "mp3" or message.audio.file_size > 2000 * 1024 * 1024:
        await message.answer("Пришлите аудио файл в формате mp3 размером до 2000мб")
        return
    data = await state.get_data()
    await add_track(message, data["album_id"], data["track_name"])
    await message.answer("Файл добавлен в викторину", reply_markup=await manage_album_btns())
    await state.set_state(ChooseAction.album.state)


async def bot_delete_track(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await delete_track(callback_query.message.chat.id, data["album_id"], callback_query.message.audio.file_name,
                       callback_query.message.caption)
    await callback_query.message.delete()
    await callback_query.message.answer("Файл удален", reply_markup=await manage_album_btns())


async def bot_share_album(message: types.Message, state: FSMContext):
    if message.text == 'Да, поделиться':
        data = await state.get_data()
        await album_make_public(data)
        await message.answer("Ссылка для добавления викторины другому пользователю:\n"
                             f"https://t.me/MusGuessTrain_bot?start={data['user_id']}_{data['album_id']}",
                             reply_markup=await manage_album_btns())
        await state.set_state(ChooseAction.album.state)
    elif message.text == 'Нет, вернуться назад':
        await message.answer("Выберите действие для викторины", reply_markup=await manage_album_btns())
        await state.set_state(ChooseAction.album.state)
    else:
        await message.answer("Неизвестная команда", reply_markup=await manage_album_btns())
        await state.set_state(ChooseAction.album.state)


async def bot_manage_album(message: types.Message, state: FSMContext):
    album_id = message.text.split()[0]
    album_name = ' '.join(message.text.split()[2:])
    await state.set_state(ChooseAction.album.state)
    await state.update_data(data={f'album_id': album_id, 'album_name': album_name, 'user_id': str(message.from_user.id)})
    await message.answer(f"Выберите действие для викторины {album_name}",
                         reply_markup=await manage_album_btns())


def register_get_album(dp: Dispatcher):
    dp.register_message_handler(bot_manage_album, regexp="^[1-9][0-9]* - .+$", state='*')
    dp.register_message_handler(bot_default_action_album, Text(["Мои викторины", "В главное меню"]), state='*')
    dp.register_message_handler(bot_action_album,  state=ChooseAction.album)
    dp.register_message_handler(bot_share_album, state=ChooseAction.share_album)
    dp.register_callback_query_handler(bot_delete_track, state=ChooseAction.album)
    dp.register_message_handler(bot_get_track_name, content_types=types.ContentType.TEXT, state=ChooseAction.track_name)
    dp.register_message_handler(bot_get_track, content_types=types.ContentType.AUDIO, state=ChooseAction.track)
