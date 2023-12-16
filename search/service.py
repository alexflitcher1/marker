from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.http_search import search_track, search_albums, search_artists


app = FastAPI(title='Marker Search APIs')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/search', tags=['Search'])
async def search(query: str):
    """ Return search results from other app modules """

    result = {}
    tracks = await search_track(query, 0, 20)
    result['tracks'] = tracks[0]
    albums = await search_albums(query, 0, 20)
    result['albums'] = albums[0]
    artists = await search_artists(query, 0, 20)
    result['artists'] = artists[0]
    return result
