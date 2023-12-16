import json
from httpx import AsyncClient

from config import TRACK_URL, ALBUM_URL, ARTIST_URL

client = AsyncClient()


async def search_track(query: str, start: int, stop: int):
    """ Make search request to tracks service """

    result = await client.get(f'{TRACK_URL}/{start}/{stop}', params={'query': query})
    r = json.loads(result.content)

    return r, result.status_code


async def search_albums(query: str, start: int, stop: int):
    """ Make search request to albums service """

    result = await client.get(f'{ALBUM_URL}/{start}/{stop}', params={'query': query})
    r = json.loads(result.content)

    return r, result.status_code


async def search_artists(query: str, start: int, stop: int):
    """ Make search request to artists service """

    result = await client.get(f'{ARTIST_URL}/{start}/{stop}', params={'query': query})
    r = json.loads(result.content)

    return r, result.status_code
