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
        'name': 'Artists',
    }
]

artists_manager = DBManagerArtist()
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


@app.get('/artists/likes', tags=['Artists'])
async def artist_likes(request: Request, response: Response):

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        likes_q = likes_manager.fetch_likes(r['auth'])
        likes = []

        for like in likes_q:
            r = await client.get(ARTISTS_URL + str(like.artistid), headers={'OAuth': oauth})
            r = json.loads(r.content)['result']
            
            artist = ArtistGet(
                id=r['id'],
                name=r['name'],
                description=r['description'],
                avatar=r['avatar'],
                background=r['background']
            )
            
            likes.append(
                LikeGet(
                    id=like.id,
                    uid=like.uid,
                    artist=artist
                )
            )

        return {'result': likes}

@app.post('/artists/likes', tags=['Artists'])
async def like_artist(request: Request, response: Response, data: LikeArtist):

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        query = likes_manager.create(uid=r['auth'], artist_id=data.artist_id)

        return {'result': query}

    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.get('/artists/{id}', tags=['Artists'])
async def artist_by_id(request: Request, response: Response, id: int):

    artist = artists_manager.fetch_id(id)
    to_ret = ArtistGet(
        id=artist.id,
        name=artist.name,
        description=artist.discription,
        avatar=artist.avatar,
        background=artist.background
    )

    return {'result': to_ret}
