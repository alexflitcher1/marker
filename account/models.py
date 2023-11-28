from pydantic import BaseModel

from utils.serializers import ModelSerializer


class SerializedModel(BaseModel, ModelSerializer):
    pass


class AccountGet(SerializedModel):

    id: int
    now: int | None
    login: str
    firstName: str | None
    lastName: str | None
    phones: int | None
    email: str
    region: int
    password: str
    role: str


class AccountCreate(SerializedModel):

    login: str
    firstName: str | None
    lastName: str | None
    email: str
    password: str


class AccountToken(SerializedModel):

    login: str
    password: str


class SettingsGet(SerializedModel):

    id: int
    uid: int
    theme: str
    lang: str
    avatar: str
    background: str


class SettingsUpdate(SerializedModel):

    theme: str | None
    lang: str | None


class MailModel(SerializedModel):

    email: str
    code: str


class TokenModel(SerializedModel):

    access_token: str
    refresh_token: str


class TokenPayload(SerializedModel):

    exp: int
    sup: str


class ServiceSettings(SerializedModel):

    authjwt_secret_key: str = "secret"
