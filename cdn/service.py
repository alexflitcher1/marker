from fastapi import FastAPI, HTTPException, status

from fastapi import Request, Body
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os.path

app = FastAPI(title='Marker Account APIs')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/img/{file}')
async def img(file: str):
    if os.path.isfile(f'./static/img/{file}'):
        return FileResponse(f'./static/img/{file}')

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Image file doens't exist", "code": 10}
    )


@app.get('/audio/{file}')
async def audio(file: str):
    if os.path.isfile(f'./static/audio/{file}'):
        return FileResponse(f'./static/audio/{file}')

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Audio file doens't exist", "code": 11}
    )


@app.get('/avatar/{file}')
async def avatar(file: str):
    if os.path.isfile(f'./static/avatars/{file}'):
        return FileResponse(f'./static/avatars/{file}')

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Avater file doens't exist", "code": 12}
    )


@app.get('/background/{file}')
async def background(file: str):
    if os.path.isfile(f'./static/background/{file}'):
        return FileResponse(f'./static/background/{file}')

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Avater file doens't exist", "code": 13}
    )


@app.get('/artist-avatar/{file}')
async def artist_avatar(file: str):
    if os.path.isfile(f'./static/artists/avatar/{file}'):
        return FileResponse(f'./static/artists/avatar/{file}')

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Avater file doens't exist", "code": 13}
    )


@app.get('/artist-background/{file}')
async def artist_background(file: str):
    if os.path.isfile(f'./static/artists/background/{file}'):
        return FileResponse(f'./static/artists/background/{file}')

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={"msg": "Avater file doens't exist", "code": 13}
    )