from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from models import ArtistGet, LikeGet, LikeArtist
from db_manager import DBManagerArtist, DBManagerLikes

import utils.auth as uauth
import utils.exception_generators as ugens


artists_manager = DBManagerArtist()
likes_manager = DBManagerLikes()

app = FastAPI(title='Marker Artists APIs')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/artists/likes', tags=['Artists'])
async def artist_likes(request: Request):
    """ Return user artists likes """

    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    likes_q = likes_manager.fetch_likes(user['id'])
    likes = []

    for like in likes_q:
        artist = artists_manager.fetch_id(like.artistid)
        if not artist:
            continue

        artist = ArtistGet(**artist.serialize)
        likes.append(
            LikeGet(
                id=like.id,
                uid=like.uid,
                artist=artist
            )
        )

    return likes


@app.post('/artists/likes', tags=['Artists'])
async def like_artist(request: Request, data: LikeArtist):
    """ Make like for artist with data.id, if it exists delete like """

    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    artist = artists_manager.fetch_id(data.artist_id)

    if not artist:
        ugens.generate_artist_404()

    if not likes_manager.fetch_like(uid=user['id'], artist_id=data.artist_id):
        query = likes_manager.create(uid=user['id'], artist_id=data.artist_id)
        return {'result': query}

    query = likes_manager.delete(uid=user['id'], artist_id=data.artist_id)

    return {'result': query}


@app.get('/artists/likes-ids')
async def likes_ids(request: Request):
    """ Return user's artist likes, but only ids """

    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    likes_q = likes_manager.fetch_likes(user['id'])
    ids = []

    for like in likes_q:
        artist = artists_manager.fetch_id(like.artistid)
        if not artist:
            continue

        ids.append(like.artistid)

    return ids


@app.get('/artists/search/{start}/{stop}', tags=['Artists'])
async def search_albums(start: int, stop: int, query: str):
    """ Search artists by search query """

    artists_q = artists_manager.search(query, start, stop)
    artists = [ArtistGet(**artist.serialize) for artist in artists_q]
    return artists


@app.get('/artists/{id}', tags=['Artists'], response_model=ArtistGet)
async def artist_by_id(id: int):
    """ Return artist data from id """

    artist = artists_manager.fetch_id(id)

    if not artist:
        ugens.generate_artist_404()

    return ArtistGet(**artist.serialize)
