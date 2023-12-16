import json

from models import TrackGet

from utils.auth import client
from config import TRACK_URL


async def unique_tracks(tracks_q):
    """ Make array with unique titles of tracks """

    tracks = []
    used = set([])

    for track in tracks_q:
        if 'trackid' in track.serialize:
            track = await client.get(TRACK_URL + str(track.trackid))
        else:
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
