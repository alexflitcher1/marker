import random
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from db import engine, Account, Settings, Mails


class DBManagerAccount:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def create(self, login: str, email: str, password: str, 
        now: int = None, region: int = 0, firstName: str = None,
        lastName: str = None, phones: int = None, role: str = 'user'):
        account = Account(
            login=login,
            password=password,
            region=region,
            firstName=firstName,
            lastName=lastName,
            phones=phones,
            email=email,
            role=role
        )

        try:
            self.db.add(account)
            self.db.commit()

            settings = Settings(uid=account.id)
            self.db.add(settings)
            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return account.id

    def fetch_login(self, login: str):
        return self.db.query(Account)\
        .filter(Account.login == login).first()

    def fetch_id(self, id: int):
        return self.db.query(Account)\
        .filter(Account.id == id).first()

    def fetch_password(self, password: str):
        return self.db.query(Account) \
        .filter(Account.password == password).first()

    def fetch_email(self, email: str):
        return self.db.query(Account) \
        .filter(Account.email == email).first()



class DBManagerSettings:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def fetch_uid(self, uid):
        return self.db.query(Settings)\
        .filter(Settings.uid==uid).first()

    def update_theme(self, uid: int, theme: str = None, lang: str = None):
        user = self.fetch_uid(uid)

        to_update = {
            'theme': theme if theme is not None else user.theme,
            'lang': lang if lang is not None else user.lang
        }
        try:
            self.db.query(Settings) \
                .filter(Settings.uid == uid) \
                .update(to_update)
            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return self.db.query(Settings) \
            .filter(Settings.uid == uid).first()


class DBManagerMails:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def create(self, email: str):
        code = random.randint(10000000, 99999999)

        mail = Mails(
            email=email,
            code=code
        )

        data = self.db.query(Mails) \
            .filter(Mails.email == email) \
            .all()

        if len(data) == 0:
            self.db.add(mail)
            self.db.commit()
        else:
            self.db.query(Mails) \
                .filter(Mails.email == email) \
                .update({'code': code})
            self.db.commit()

        return code

    def fetch_code(self, email: str):
        to_ret = self.db.query(Mails) \
            .filter(Mails.email == email) \
            .first()

        return to_ret

    def delete_code(self, email: str):
        try:
            code = self.fetch_code(email).code

            self.db.query(Mails) \
                .filter(Mails.email == email) \
                .delete()

            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return code
