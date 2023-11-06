from pydantic import BaseModel, Field


class AlbumGet(BaseModel):
    
    id: int
    artistid: int
    title: str
    description: str
    avatar: str
    genre: str

class LikeGet(BaseModel):

    id: int
    uid: int
    album: AlbumGet

class LikeAlbum(BaseModel):
    
    album_id: int