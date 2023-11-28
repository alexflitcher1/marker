from pydantic import BaseModel, Field

from utils.serializers import ModelSerializer


class SerializedModel(BaseModel, ModelSerializer):
    pass


class ArtistGet(SerializedModel):
    
    id: int
    name: str
    description: str
    avatar: str
    background: str


class TrackGet(SerializedModel):
    
    id: int
    title: str
    artists: list[ArtistGet]
    albumid: int
    avatar: str
    path: str
    genre: str


class LikeGet(SerializedModel):

    id: int
    uid: int
    track: TrackGet


class LikeTrack(SerializedModel):

    track_id: int


class Error(SerializedModel):
    
    code: int
    message: str