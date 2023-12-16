import json
import pika

from fastapi import FastAPI, Depends, Request
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.middleware.cors import CORSMiddleware

from models import AccountGet, AccountCreate, AccountToken, SettingsGet
from models import SettingsUpdate, MailModel, TokenModel, ServiceSettings
from db_manager import DBManagerAccount, DBManagerSettings, DBManagerMails

import utils.auth as uauth
import utils.exception_generators as ugens
import utils.validation as uvalid


account_manager = DBManagerAccount()
settings_manager = DBManagerSettings()
email_manager = DBManagerMails()

app = FastAPI(title='Marker Account APIs')

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@AuthJWT.load_config
def get_config():
    return ServiceSettings()


@app.get('/account/auth', tags=['Account'], response_model=AccountGet)
async def auth(user: AccountToken = Depends(uauth.is_auth)):
    user = account_manager.fetch_email(user['sub'])
    return AccountGet(**user.serialize)


@app.get('/account/status', tags=['Account'], response_model=AccountGet)
async def status(request: Request):

    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    return AccountGet(**user)


@app.get('/account/settings', tags=['Account'])
async def settings_get(request: Request):

    user, code, token = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    settings = settings_manager.fetch_uid(user['id'])
    return SettingsGet(**settings.serialize)


@app.post('/account/settings', tags=['Account'], response_model=SettingsGet)
async def settings_change(request: Request, data: SettingsUpdate):

    user, code, _ = await uauth.is_auth_query(request)

    if code != 200:
        ugens.generate_401()

    args = {
        'uid': user['id'],
        'theme': data.theme,
        'lang': data.lang
    }
    settings = settings_manager.update_theme(**args)
    return SettingsGet(**settings.serialize)


@app.post('/account/mail', tags=['Account'])
async def mail(data: AccountCreate):

    if not uvalid.validate(data):
        ugens.generate_code_400()

    # check that user data is not already used
    account_check = (
        account_manager.fetch_email(data.email),
        account_manager.fetch_login(data.login)
    )
    if account_check[0]:
        ugens.generate_mail_400()

    if account_check[1]:
        ugens.generate_login_400()

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
    severity = '/account/mail'

    code = email_manager.create(data.email)
    message = json.dumps({'email': data.email, 'code': code})
    channel.basic_publish(
        exchange='direct_logs', routing_key=severity, body=message)

    connection.close()
    return {'result': bool(code)}


@app.post('/account/create', tags=['Account'], response_model=AccountCreate)
async def create(user: AccountCreate, mail: MailModel):

    code = email_manager.fetch_code(mail.email)

    try:
        code = code.code
        if mail.email != user.email or code != mail.code:
            raise Exception()
    except Exception:
        ugens.generate_code_400()

    password = uauth.get_hashed_password(user.password)
    user.password = password

    account_manager.create(**user.serialize)
    email_manager.delete_code(email=mail.email)

    return AccountCreate(**user.serialize)


@app.post('/account/token', tags=['Account'], response_model=TokenModel)
async def token(user: AccountToken, Authorize: AuthJWT = Depends()):

    account = account_manager.fetch_login(user.login)
    if not user or not account:
        ugens.generate_token_400()

    password_hash = account.password

    if not uauth.verify_password(user.password, password_hash):
        ugens.generate_token_400()

    tokens = TokenModel(
        access_token=Authorize.create_access_token(subject=account.email),
        refresh_token=Authorize.create_refresh_token(subject=account.email)
    )

    return tokens


@app.post('/account/refresh')
def refresh(Authorize: AuthJWT = Depends()):

    try:
        Authorize.jwt_refresh_token_required()
        current_user = Authorize.get_jwt_subject()
        new_access_token = Authorize.create_access_token(subject=current_user)
        return {"access_token": new_access_token}
    except AuthJWTException:
        ugens.generate_401()
