import json
from config import *

import httpx
from httpx import AsyncClient

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from fastapi import Depends
from fastapi import HTTPException, status
from pydantic import ValidationError
from fastapi.security import OAuth2PasswordBearer
from models import TokenPayload

client = AsyncClient()
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

reuseable_oauth = OAuth2PasswordBearer(
    tokenUrl="/account/token",
    scheme_name="JWT"
)


async def is_auth(token: str = Depends(reuseable_oauth)):
    try:
        payload = jwt.decode(
            token, JWT_SECRET_KEY, algorithms=[ALGORITHM]
        )
        
        if datetime.fromtimestamp(payload['exp']) < datetime.now():
            raise HTTPException(
                status_code = status.HTTP_401_UNAUTHORIZED,
                detail={"msg": "Token expired", "code": 2},
                headers={"WWW-Authenticate": "Bearer"},
            )
    except:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"msg": "Could not validate credentials", "code": 4},
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def is_auth_query(request):
    auth = request.headers.get('Authorization')

    if not auth:
        return (False, False, False)
    
    result = await client.get(AUTH_URL, headers={'Authorization': auth})
    r = json.loads(result.content)

    return (r, result.status_code, auth)


def create_access_token(subject: 'str', expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: 'str', expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def get_hashed_password(password: str):
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str):
    return password_context.verify(password, hashed_pass)