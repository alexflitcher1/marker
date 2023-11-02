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
        'name': 'Tracks',
    }
]

tracks_manager = DBManagerTracks()
likes_manager = DBManagerLikes()

app = FastAPI(
    title='Marker APIs',
    openapi_tags=tags_metadata
)

client = AsyncClient()


@app.get('/tracks/likes', tags=['Tracks'])
async def likes_user(request: Request, response: Response):
    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        likes_q = likes_manager.fetch_likes(r['auth'])
        likes = []

        for like in likes_q:
            r = await client.get('http://localhost:8002/tracks/' + str(like.trackid), headers={'OAuth': oauth})
            r = json.loads(r.content)['result']
            
            track = TrackGet(
                id=r['id'],
                title=r['title'],
                artists=r['artists'],
                albumid=r['albumid'],
                avatar=r['avatar'],
                path=r['path']
            )

            likes.append(
                LikeGet(
                    id=like.id,
                    uid=like.uid,
                    track=track
                )
            )
        
        return {'result': likes}

    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.post('/tracks/likes', tags=['Tracks'])
async def like_track(request: Request, response: Response, data: LikeTrack):
    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        query = likes_manager.create(uid=r['auth'], track_id=data.track_id)

        return {'result': query}

    response.status_code = 401
    return {'error': 'Unauthorized'}

@app.get('/tracks/{id}', tags=['Tracks'])
async def track_by_id(request: Request, response: Response, id: int):

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        track = tracks_manager.fetch_id(id)
        album_id = track.albumid
        title = track.title

        artists_q = tracks_manager.fetch_with_artists(album_id, title)
        artists = []
        for artist in artists_q:
            r = await client.get(ARTIST_URL + str(artist.artistid), headers={'OAuth': oauth})
            r = json.loads(r.content)['result']
            artists.append(
                ArtistGet(
                    id=r['id'],
                    name=r['name'],
                    description=r['description'],
                    avatar=r['avatar'],
                    background=r['background']
                )
            )

        to_ret = TrackGet(
            id=track.id,
            title=track.title,
            artists=artists,
            albumid=track.albumid,
            avatar=track.avatar,
            path=track.path
        )

        return {'result': to_ret}
    
    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.get('/tracks/album/{id}', tags=['Tracks'])
async def track_by_id(request: Request, response: Response, id: int):

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        album = await client.get(ALBUM_URL + str(id), headers={'OAuth': oauth})
        album = json.loads(album.content)
        
        album_id = album['result']['id']

        tracks_q = tracks_manager.fetch_tracks(album_id)
        tracks = []

        for track in tracks_q:
            track = await client.get(TRACK_URL + str(track.id), headers={'OAuth': oauth})
            track = json.loads(track.content)

            tracks.append(track['result'])

        del album['result']['artistid']
        album['result']['tracks'] = tracks
        return {'result': album['result']}
    
    response.status_code = 401
    return {'error': 'Unauthorized'}
