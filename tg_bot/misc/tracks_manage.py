from aiofiles import os, open
import json
import random
from pydub import AudioSegment


async def move_file(source, destination):
    async with open(source, 'rb') as f_src:
        async with open(destination, 'wb') as f_dst:
            content = await f_src.read()
            await f_dst.write(content)
    await os.remove(source)


async def delete_track_fragment(user_id, album_id, track_name_mp3):
    await os.remove(f"music_data/{user_id}/{album_id}/{track_name_mp3}")


async def get_track_fragment(user_id, album_id, track_name_mp3):
    track = AudioSegment.from_file(f"music_data/{user_id}/{album_id}/{track_name_mp3}", format="mp3")
    random_second = random.randint(0, int(track.duration_seconds) - 15)
    random_15_seconds = track[random_second * 1000: (random_second + 15) * 1000]
    name = 'random_15_seconds.mp3'
    random_15_seconds.export(f"music_data/{user_id}/{album_id}/{name}", format="mp3")
    return name


async def get_tracks(user_id, album_id):
    if not await os.path.exists(f"music_data/{user_id}/{album_id}/names.json"):
        return dict()
    async with open(f"music_data/{user_id}/{album_id}/names.json", mode='r', encoding='utf-8') as f:
        tracks = json.loads(await f.readline())
    return tracks


async def tracks_count(user_id, album_id):
    return len(await get_tracks(user_id, album_id))


async def add_track(message, album_id, track_name):
    user_id = message.from_user.id
    track_name = track_name.replace('\n', ' ').replace('\t', ' ').replace('-', ' ').replace('—', ' ')
    track_name_mp3 = track_name.replace(' ', '-') + '.mp3'
    file = await message.bot.get_file(message.audio["file_id"])
    await move_file(file.file_path, f"music_data/{user_id}/{album_id}/{track_name_mp3}")
    tracks = await get_tracks(user_id, album_id)
    tracks.update({track_name: track_name_mp3})
    async with open(f"music_data/{user_id}/{album_id}/names.json", mode='w', encoding='utf-8') as f:
        await f.write(json.dumps(tracks))


async def delete_track(user_id, album_id, track_name, key):
    await os.remove(f"music_data/{user_id}/{album_id}/{track_name}")
    if await tracks_count(user_id, album_id) == 1:
        await os.remove(f"music_data/{user_id}/{album_id}/names.json")
        return
    tracks = await get_tracks(user_id, album_id)
    tracks.pop(key)
    async with open(f"music_data/{user_id}/{album_id}/names.json", mode='w', encoding='utf-8') as f:
        await f.write(json.dumps(tracks))
