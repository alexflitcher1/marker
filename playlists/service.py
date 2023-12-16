from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from models import PlaylistGet, PlaylistCreate, PlaylistUpdate, TrackAdd

import utils.auth as uauth
import utils.queries as uque
import utils.exception_generators as ugens

from db_manager import DBManagerPlaylists, DBManagerTracks

playlists_manager = DBManagerPlaylists()
tracks_manager = DBManagerTracks()

app = FastAPI(title="Playlists Marker API's")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/playlists/{pid}')
async def playlist_by_id(request: Request, pid: int):
    """ Return playlist without tracks by id """
    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    playlist = playlists_manager.fetch_id(pid)

    if playlist:
        return PlaylistGet(**playlist.serialize)

    ugens.generate_404()


@app.post('/playlists/create')
async def playlist_create(request: Request, data: PlaylistCreate):
    """ Create playlist """
    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    data = data.serialize
    data['uid'] = user['id']

    pid = playlists_manager.create(**data)
    data['id'] = pid
    if pid:
        return data

    ugens.generate_500()


@app.post('/playlists/delete/{pid}')
async def playlist_delete(request: Request, pid: int):
    """ Delete playlist by id """
    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    if playlists_manager.fetch_id(pid).uid != user['id']:
        return ugens.generate_401()

    return playlists_manager.delete(pid)


@app.post('/playlists/update')
async def playlist_update(request: Request, data: PlaylistUpdate):
    """ Update playlist data by data.id """
    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    if playlists_manager.fetch_id(data.pid).uid != user['id']:
        return ugens.generate_401()

    result = playlists_manager.update(**data.serialize)

    return PlaylistGet(**result.serialize)


@app.get('/playlists/tracks/{start}/{stop}')
async def playlist_tracks(pid: int, start: int, stop: int):
    """ Return tracks with data from `start` to `stop` from playlist with `pid` """
    tracks_q = tracks_manager.fetch_tracks(pid, start, stop)
    tracks = await uque.unique_tracks(tracks_q)

    return tracks


@app.post('/playlists/tracks')
async def playlist_add_track(request: Request, data: TrackAdd):
    """ Add or remove track in playlist """
    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    if playlists_manager.fetch_id(data.pid).uid != user['id']:
        return ugens.generate_401()

    if tracks_manager.fetch_track(data.pid, data.tid):
        return tracks_manager.delete(data.pid, data.tid)

    return tracks_manager.create(data.pid, data.tid)


@app.get('/playlists')
async def playlists_by_uid(request: Request):
    """ Return all user's playlists """
    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    playlists_q = playlists_manager.fetch_uid(user['id'])
    playlists = [PlaylistGet(**playlist.serialize) for playlist in playlists_q]

    return playlists
