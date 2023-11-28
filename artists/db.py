from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

from utils.serializers import TableSerializer


SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://x:1234@localhost:5432/artists"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase, TableSerializer):
    pass


class Artist(Base):
    __tablename__ = "artist"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128))
    description = Column(String(512))
    avatar = Column(String(128))
    background = Column(String(128))


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artistid = Column(Integer)
    uid = Column(Integer)


Base.metadata.create_all(bind=engine)