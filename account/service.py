from fastapi import FastAPI
from fastapi import Request, Body
from fastapi import Response
from fastapi.middleware.cors import CORSMiddleware

import httpx
from httpx import AsyncClient
import json

import bcrypt

import pika

from models import *
from db_manager import *
from config import *


tags_metadata = [
    {
        'name': 'Account',
    }
]

account_manager = DBManagerAccount()
settings_manager = DBManagerSettings()
email_manager = DBManagerMails()

app = FastAPI(
    title='Marker APIs',
    openapi_tags=tags_metadata
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncClient()


@app.get('/account/auth', tags=['Account'])
async def auth(request: Request, response: Response):

    oauth = request.headers.get('OAuth')
    account = account_manager.fetch_password(oauth)

    if account:
        return {'auth': account.id}
    
    response.status_code = 401
    return {'auth': False}


@app.get('/account/status', tags=['Account'])
async def status(request: Request, response: Response):

    oauth = request.headers.get('OAuth')

    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        account = account_manager.fetch_password(oauth)
        to_ret = AccountGet(
            id=account.id,
            now=account.now,
            login=account.login,
            firstName=account.firstName,
            lastName=account.lastName,
            phones=account.phones,
            email=account.email,
            region=account.region,
            password=account.password,
            role=account.role
        )
        return {'result': to_ret}

    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.get('/account/settings', tags=['Account'])
async def settings(request: Request, response: Response):
    
    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)
    
    if r['auth']:
        account = account_manager.fetch_password(oauth)
        settings = settings_manager.fetch_uid(account.id)
        to_ret = SettingsGet(
            id=settings.id,
            uid=settings.uid,
            theme=settings.theme
        )
        return {'result': to_ret}

    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.post('/account/settings', tags=['Account'])
async def settings(request: Request, response: Response, data: SettingsUpdate):

    oauth = request.headers.get('OAuth')
    
    r = await client.get(AUTH_URL, headers={'OAuth': oauth})
    r = json.loads(r.content)

    if r['auth']:
        account = account_manager.fetch_password(oauth)
        to_ret = settings_manager.update_theme(
            uid=account.id,
            theme=data.theme
        )
        response.status_code = 201
        return to_ret

    response.status_code = 401
    return {'error': 'Unauthorized'}


@app.post('/account/mail', tags=['Account'])
async def mail(request: Request, response: Response, data: AccountCreate):
    
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()
    
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    severity = '/account/mail'

    
    code = email_manager.create(email=data.email)

    message = json.dumps({'email': data.email, 'code': code})
    channel.basic_publish(
        exchange='direct_logs', routing_key=severity, body=message)

    connection.close()

    return {'result': bool(code)}


@app.post('/account/create', tags=['Account'])
async def create(request: Request, response: Response, user: AccountCreate, mail: MailModel):
    
    code = email_manager.fetch_code(email=mail.email).code

    if mail.email == user.email and code == mail.code:
       password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt()).decode()
       account_manager.create(
            login=user.login,
            email=user.email,
            password=password,
            firstName=user.firstName,
            lastName=user.lastName
       )
       email_manager.delete_code(email=mail.email)
       return {'result': password}

    return {'error': 'Mail code is not valid'}


@app.post('/account/token', tags=['Account'])
async def token(request: Request, response: Response, user: AccountToken):
    
    login = account_manager.fetch_login(user.login)
    password = login.password

    if bcrypt.hashpw(user.password.encode(), password.encode()).decode() == password:
        return {'result': password }
    
    return {'result': False}
