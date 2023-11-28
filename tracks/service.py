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
import utils.auth as uauth
import utils.exception_generators as ugens
from utils.auth import client


tracks_manager = DBManagerTracks()
likes_manager = DBManagerLikes()

app = FastAPI(title='Marker Tracks APIs')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/tracks/likes', tags=['Tracks'])
async def likes_user(request: Request):
    
    user, code, token = await uauth.is_auth_query(request)
    
    if code != 200:
        ugens.generate_401()

    likes_q = likes_manager.fetch_likes(user['id'])
    likes = []

    for like in likes_q:
        track = await client.get(TRACK_URL + str(like.trackid))
        if track.status_code != 200:
            continue

        track = json.loads(track.content)
            
        track = TrackGet(**track)

        likes.append(track)
        
    return likes

@app.get('/tracks/likes-ids')
async def likes_ids(request: Request):
    user, code, token = await uauth.is_auth_query(request)
    
    if code != 200:
        ugens.generate_401()

    likes_q = likes_manager.fetch_likes(user['id'])
    ids = []

    for like in likes_q:
        track = await client.get(TRACK_URL + str(like.trackid))
        if track.status_code != 200:
            continue

        ids.append(like.trackid)

    return ids


@app.post('/tracks/likes', tags=['Tracks'])
async def like_track(request: Request, data: LikeTrack):
    
    user, code, token = await uauth.is_auth_query(request)
    
    if code != 200:
        ugens.generate_401()


    track = tracks_manager.fetch_id(data.track_id)

    if not track:
        ugens.generate_track_404()
    
    if not likes_manager.fetch_like(uid=user['id'], track_id=data.track_id):
        query = likes_manager.create(uid=user['id'], track_id=data.track_id)
        return {'result': query}
    
    query = likes_manager.delete(uid=user['id'], track_id=data.track_id)
    return  {'result': query}


@app.get('/tracks/pagination/{start}/{stop}', tags=['Tracks'])
async def pagination(start: int, stop: int):

    tracks_q = tracks_manager.fetch_pagination(start, stop)

    tracks = []

    used = set([])

    for track in tracks_q:
        track = await client.get(TRACK_URL + str(track.id))
        if track.status_code != 200:
            continue

        track = json.loads(track.content)
        
        if track['title'] in used:
            continue

        used.add(track['title'])

        track = TrackGet(**track)

        tracks.append(track)

    return tracks


@app.get('/tracks/{id}', tags=['Tracks'], response_model=TrackGet)
async def track_by_id(id: int):
    
    track = tracks_manager.fetch_id(id)

    if not track:
        ugens.generate_track_404()

    album_id = track.albumid
    title = track.title

    artists_q = tracks_manager.fetch_with_artists(album_id, title)
    artists = []

    for artist in artists_q:
        artist = await client.get(ARTIST_URL + str(artist.artistid))
        if artist.status_code != 200:
            continue
        
        artist = json.loads(artist.content)
        artists.append(ArtistGet(**artist))

    track_serialize = track.serialize
    track_serialize['artists'] = artists
    del track_serialize['artistid']

    return TrackGet(**track_serialize)
    

@app.get('/tracks/album/{id}', tags=['Tracks'])
async def track_by_id(id: int):

    album = await client.get(ALBUM_URL + str(id))

    if album.status_code == 404:
        return json.loads(album.content)

    album = json.loads(album.content)
    album_id = album['id']

    tracks_q = tracks_manager.fetch_tracks(album_id)
    tracks = []

    titles = set([])
    
    for track in tracks_q:
        track = await client.get(TRACK_URL + str(track.id))
        track = json.loads(track.content)

        if track['title'] in titles:
            continue

        titles.add(track['title'])

        tracks.append(track)

    del album['artistid']
    album['tracks'] = tracks

    return album


@app.get('/tracks/artist/{id}/{start}/{stop}', tags=['Tracks'])
async def track_by_id(id: int, start: int, stop: int):

    tracks_q = tracks_manager.fetch_artist_tracks(id, start, stop)

    tracks = []

    used = set([])

    for track in tracks_q:
        track = await client.get(TRACK_URL + str(track.id))
        if track.status_code != 200:
            continue

        track = json.loads(track.content)
        if track['title'] in used:
            continue

        used.add(track['title'])
        
        track = TrackGet(**track)
        tracks.append(track)

    return tracks