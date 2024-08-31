from aiofiles import os, open
import json
import shutil


async def get_albums(user_id):
    if not await os.path.exists(f"music_data/{user_id}/names.json"):
        return dict()
    async with open(f"music_data/{user_id}/names.json", mode='r', encoding='utf-8') as f:
        albums = json.loads(await f.readline())
    return albums


async def get_public_albums():
    if not await os.path.exists(f"music_data/public.json"):
        return list()
    async with open("music_data/public.json", mode='r', encoding='utf-8') as f:
        albums = json.loads(await f.readline())
    return albums["public_albums"]


async def album_is_public(user_id, album_id):
    albums = await get_public_albums()
    for album in albums:
        if album["album_id"] == album_id and album["user_id"] == user_id:
            return album["album_name"]
    return str()


async def add_public_album(user_id, from_user_id, album_id):
    if from_user_id == str(user_id):
        return "Извините, вы не можете добавлять свою викторину"
    albums_cnt = await albums_count(user_id)
    if albums_cnt >= 32:
        return "Извините, вы не можете добавлять больше 32 викторин"
    album_name = await album_is_public(from_user_id, album_id)
    if album_name:
        albums = await get_albums(user_id)
        albums.update({str(albums_cnt + 1): album_name})
        if not await os.path.exists(f"music_data/{user_id}"):
            await os.mkdir(f"music_data/{user_id}")
        async with open(f"music_data/{user_id}/names.json", mode='w', encoding='utf-8') as f:
            await f.write(json.dumps(albums)) 
        shutil.copytree(f"music_data/{from_user_id}/{album_id}", f"music_data/{user_id}/{albums_cnt + 1}")
        return f"Викторина {album_name} успешно добавлена"
    return "Викторина не найдена"


async def albums_count(user_id):
    return len(await get_albums(user_id))


async def add_album(user_id, album_name):
    cnt = await albums_count(user_id)
    if not await os.path.exists(f"music_data/{user_id}/"):
        await os.mkdir(f"music_data/{user_id}/")
    albums = await get_albums(user_id)
    albums.update({str(cnt + 1): album_name})
    async with open(f"music_data/{user_id}/names.json", mode='w', encoding='utf-8') as f:
        await f.write(json.dumps(albums))
    await os.mkdir(f"music_data/{user_id}/{cnt + 1}/")


async def delete_album(user_id, album_id):
    cnt = await albums_count(user_id)
    shutil.rmtree(f"music_data/{user_id}/{album_id}")
    if cnt == 1:
        await os.remove(f"music_data/{user_id}/names.json")
        return
    for cn in range(int(album_id) + 1, cnt + 1):
        await os.rename(f"music_data/{user_id}/{cn}", f"music_data/{user_id}/{cn - 1}")
    albums = await get_albums(user_id)
    albums.pop(album_id)
    albums = {alb_id if int(alb_id) < int(album_id) else str(int(alb_id) - 1): alb_name for alb_id, alb_name in albums.items()}
    async with open(f"music_data/{user_id}/names.json", mode='w', encoding='utf-8') as f:
        await f.write(json.dumps(albums))


async def album_make_public(data):
    public_albums = await get_public_albums()
    if data not in public_albums:
        public_albums.append(data)
    async with open("music_data/public.json", mode='w', encoding='utf-8') as f:
        await f.write(json.dumps({"public_albums": public_albums}))