from pydantic import BaseModel, Field

class ArtistGet(BaseModel):
    
    id: int
    name: str
    description: str
    avatar: str
    background: str

class TrackGet(BaseModel):
    
    id: int
    title: str
    artists: list[ArtistGet]
    albumid: int
    avatar: str
    path: str

class LikeGet(BaseModel):

    id: int
    uid: int
    track: TrackGet

class LikeTrack(BaseModel):

    track_id: int