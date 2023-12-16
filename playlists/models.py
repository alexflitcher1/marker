from pydantic import BaseModel, Field

from utils.serializers import ModelSerializer


class SerializedModel(BaseModel, ModelSerializer):
    pass


class PlaylistGet(SerializedModel):

    id: int
    uid: int
    title: str
    avatar: str
    description: str


class PlaylistCreate(SerializedModel):

    title: str | None
    avatar: str | None
    description: str | None


class PlaylistUpdate(SerializedModel):

    pid: int
    title: str | None
    description: str | None


class TrackAdd(SerializedModel):

    pid: int
    tid: int


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
