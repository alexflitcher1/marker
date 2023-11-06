from fastapi import FastAPI
from fastapi import Request, Body
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware

import httpx
from httpx import AsyncClient
import json

from models import *
from db_manager import *
from config import *


tags_metadata = [
    {
        'name': 'Albums',
    }
]

album_manager = DBManagerAlbum()
likes_manager = DBManagerLikes()

app = FastAPI(
    title='Marker APIs',
    openapi_tags=tags_metadata
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncClient()

@app.get('/albums/likes', tags=['Albums'])
async def album_likes(request: Request, response: Response):
    
    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        likes_q = likes_manager.fetch_likes(r['auth'])
        likes = []

        for like in likes_q:
            r = await client.get(ALBUM_URL + str(like.albumid), headers={'OAuth': oauth})
            r = json.loads(r.content)['result']
            
            album = AlbumGet(
                id=r['id'],
                artistid=r['artistid'],
                title=r['title'],
                description=r['description'],
                avatar=r['avatar'],
                genre=r['genre']
            )

            likes.append(
                LikeGet(
                    id=like.id,
                    uid=like.uid,
                    album=album
                )
            )

        return {'result': likes}


@app.post('/albums/likes', tags=['Albums'])
async def like_album(request: Request, response: Response, data: LikeAlbum):

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        query = likes_manager.create(uid=r['auth'], album_id=data.album_id)

        return {'result': query}

    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.get('/albums/{id}', tags=['Albums'])
async def album_by_id(request: Request, response: Response, id: int):
        
    album = album_manager.fetch_id(id)
    to_ret = AlbumGet(
        id=album.id,
        artistid=album.artistid,
        title=album.title,
        description=album.discription,
        avatar=album.avatar,
        genre=album.genre
    )

    return {'result': to_ret}


@app.get('/albums/artist/{id}', tags=['Albums'])
async def album_tracks(request: Request, response: Response, id: int):

    albums_q = album_manager.fetch_artist_id(id)
    albums = []
    
    for album in albums_q:
        albums.append(
            AlbumGet(
                id=album.id,
                artistid=album.artistid,
                title=album.title,
                description=album.discription,
                avatar=album.avatar,
                genre=album.genre
            )
        )

    return {'result': albums}