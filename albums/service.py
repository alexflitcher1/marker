from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from models import AlbumGet, LikeGet, LikeAlbum
from db_manager import DBManagerAlbum, DBManagerLikes

import utils.auth as uauth
import utils.exception_generators as ugens


album_manager = DBManagerAlbum()
likes_manager = DBManagerLikes()


app = FastAPI(title='Marker Albums APIs',)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/albums/likes', tags=['Albums'])
async def album_likes(request: Request):
    """ Return user album likes """

    user, code, _ = await uauth.is_auth_query(request)
    if code != 200:
        ugens.generate_401()

    likes_q = likes_manager.fetch_likes(user['id'])
    likes = []

    for like in likes_q:
        album_r = album_manager.fetch_id(like.albumid)
        if not album_r:
            continue

        album = AlbumGet(**album_r.serialize)
        likes.append(LikeGet(id=like.id, uid=like.uid, album=album))

    return likes


@app.post('/albums/likes', tags=['Albums'])
async def like_album(request: Request, data: LikeAlbum):
    """ Make like for album with data.id, if it exists delete like """

    user, code, _ = await uauth.is_auth_query(request)
    if code != 200:
        ugens.generate_401()

    album = album_manager.fetch_id(data.album_id)
    if not album:
        ugens.generate_album_404()

    if not likes_manager.fetch_like(uid=user['id'], album_id=data.album_id):
        query = likes_manager.create(uid=user['id'], album_id=data.album_id)
        return {'result': query}

    query = likes_manager.delete(uid=user['id'], album_id=data.album_id)

    return {'result': query}


@app.get('/albums/likes-ids')
async def likes_ids(request: Request):
    """ Return user's album likes, but only ids """

    user, code, _ = await uauth.is_auth_query(request)
    if code != 200:
        ugens.generate_401()

    likes_q = likes_manager.fetch_likes(user['id'])
    ids = []

    for like in likes_q:
        album = album_manager.fetch_id(like.albumid)
        if not album:
            continue

        ids.append(like.albumid)

    return ids


@app.get('/albums/search/{start}/{stop}', tags=['Albums'])
async def search_albums(start: int, stop: int, query: str):
    """ Search albums by search query """

    albums_q = album_manager.search(query, start, stop)
    albums = [AlbumGet(**album.serialize) for album in albums_q]
    return albums


@app.get('/albums/{id}', tags=['Albums'], response_model=AlbumGet)
async def album_by_id(id: int):
    """ Return album data without tracks """

    album = album_manager.fetch_id(id)
    if not album:
        ugens.generate_album_404()

    return AlbumGet(**album.serialize)


@app.get('/albums/artist/{id}', tags=['Albums'])
async def album_tracks(id: int):
    """ Return all artist albums without tracks """

    albums_q = album_manager.fetch_artist_id(id)
    albums = []

    for album in albums_q:
        albums.append(AlbumGet(**album.serialize))

    return albums
