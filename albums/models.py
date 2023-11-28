from pydantic import BaseModel, Field

from utils.serializers import ModelSerializer


class SerializedModel(BaseModel, ModelSerializer):
    pass


class AlbumGet(SerializedModel):
    
    id: int
    artistid: int
    title: str
    description: str
    avatar: str
    genre: str


class LikeGet(SerializedModel):

    id: int
    uid: int
    album: AlbumGet


class LikesGet(SerializedModel):

    likes: list


class LikeAlbum(SerializedModel):
    
    album_id: int


class Error(SerializedModel):
    
    code: int
    message: str