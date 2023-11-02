from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://x:1234@localhost:5432/accounts"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Base(DeclarativeBase):
    pass

class Account(Base):
    __tablename__ = "account"

    id = Column(Integer, primary_key=True, autoincrement=True)
    now = Column(Integer)
    login = Column(String(64), primary_key=True, unique=True)
    password = Column(String)
    region = Column(Integer)
    firstName = Column(String(64))
    lastName = Column(String(64))
    phones = Column(Integer)
    email = Column(String(64), primary_key=True, unique=True)
    role = Column(String(32), default="user")

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer, primary_key=True, unique=True)
    theme = Column(String(16), default='white')

class Mails(Base):
    __tablename__ = "mails"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, primary_key=True, unique=True)
    code = Column(String(12))

Base.metadata.create_all(bind=engine)