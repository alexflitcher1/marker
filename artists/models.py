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


class LikeGet(SerializedModel):

    id: int
    uid: int
    artist: ArtistGet


class LikeArtist(SerializedModel):

    artist_id: int


class Error(SerializedModel):
    
    code: int
    message: str