import json

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from models import ArtistGet, TrackGet, LikeTrack
from db_manager import DBManagerTracks, DBManagerLikes
from config import ARTIST_URL, ALBUM_URL, TRACK_URL

import utils.auth as uauth
import utils.exception_generators as ugens
from utils.auth import client

import utils.queries as uque

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
    """ Return user's likes """

    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    likes_q = likes_manager.fetch_likes(user['id'])
    likes = await uque.unique_tracks(likes_q)

    return likes


@app.get('/tracks/likes-ids')
async def likes_ids(request: Request):
    """ Return user's likes, but only ids """

    user, code, _ = await uauth.is_auth_query(request)

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
    """ Make like for track with data.id, if it exists delete like """

    user, code, _ = await uauth.is_auth_query(request)

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
    """ Return tracks from [start] to [stop] """

    tracks_q = tracks_manager.fetch_pagination(start, stop)
    tracks = await uque.unique_tracks(tracks_q)
    return tracks


@app.get('/tracks/search/{start}/{stop}', tags=['Tracks'])
async def search_tracks(start: int, stop: int, query: str):
    """ Search tracks by search query """

    tracks_q = tracks_manager.search(query, start, stop)
    tracks = await uque.unique_tracks(tracks_q)
    return tracks


@app.get('/tracks/{track_id}', tags=['Tracks'], response_model=TrackGet)
async def track_by_id(track_id: int):
    """ Return track by id """

    track = tracks_manager.fetch_id(track_id)

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


@app.get('/tracks/album/{album_id}', tags=['Tracks'])
async def album_tracks_by_id(album_id: int):
    """ Return all tracks from album with this id """

    album = await client.get(ALBUM_URL + str(album_id))
    if album.status_code == 404:
        return json.loads(album.content)

    album = json.loads(album.content)
    album_id = album['id']

    tracks_q = tracks_manager.fetch_tracks(album_id)
    tracks = await uque.unique_tracks(tracks_q)

    del album['artistid']
    album['tracks'] = tracks

    return album


@app.get('/tracks/artist/{artist_id}/{start}/{stop}', tags=['Tracks'])
async def artist_tracks_by_id(artist_id: int, start: int, stop: int):
    """ Return all artist's tracks with pagination from [start] to [stop] """

    tracks_q = tracks_manager.fetch_artist_tracks(artist_id, start, stop)
    tracks = await uque.unique_tracks(tracks_q)

    return tracks
