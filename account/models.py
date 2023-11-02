from pydantic import BaseModel

class AccountGet(BaseModel):
   
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

class AccountCreate(BaseModel):
    
    login: str
    firstName: str | None
    lastName: str | None
    email: str
    password: str

class SettingsGet(BaseModel):

    id: int
    uid: int
    theme: str

class SettingsUpdate(BaseModel):
    
    theme: str | None

class MailModel(BaseModel):

    email: str
    code: str