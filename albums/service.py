from fastapi import FastAPI
from fastapi import Request, Body
from fastapi import Response

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

client = AsyncClient()

@app.get('/albums/likes')
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
                avatar=r['avatar']
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

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        album = album_manager.fetch_id(id)
        to_ret = AlbumGet(
            id=album.id,
            artistid=album.artistid,
            title=album.title,
            description=album.discription,
            avatar=album.avatar
        )

        return {'result': to_ret}

    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.get('/albums/{id}/tracks', tags=['Albums'])
async def album_tracks(request: Request, response: Response, id: int):

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        return {'result': 'waiting'}