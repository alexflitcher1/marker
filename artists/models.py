from pydantic import BaseModel, Field


class ArtistGet(BaseModel):
    
    id: int
    name: str
    description: str
    avatar: str
    background: str

class LikeGet(BaseModel):

    id: int
    uid: int
    artist: ArtistGet

class LikeArtist(BaseModel):

    artist_id: int