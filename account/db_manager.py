from sqlalchemy.orm import sessionmaker
from db import engine, Account, Settings, Mails
import random

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

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

            return account.id
        except:
            return False

    def fetch_login(self, login: str):
        return self.db.query(Account)\
        .filter(Account.login == login).first()

    def fetch_id(self, id: int):
        return self.db.query(Account)\
        .filter(Account.id == id).first()

    def fetch_password(self, password: str):
        return self.db.query(Account) \
        .filter(Account.password == password).first()



class DBManagerSettings:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def fetch_uid(self, uid):
        return self.db.query(Settings)\
        .filter(Settings.uid==uid).first()

    def update_theme(self, uid: int, theme: str):
        try:
            self.db.query(Settings) \
                .filter(Settings.uid == uid) \
                .update({'theme': theme})
            self.db.commit()

            return self.db.query(Settings) \
                .filter(Settings.uid == uid).first()
        except:
            return False


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
        
        if not len(data):
            self.db.add(mail)
            self.db.commit()

            return code
        
        return False

    def fetch_code(self, email: str):
        to_ret = self.db.query(Mails) \
            .filter(Mails.email == email) \
            .first()
        
        try:
            code = to_ret.code
        
            self.db.query(Mails) \
                .filter(Mails.email == email) \
                .delete()

            self.db.commit()

            return code
        except:
            return False
