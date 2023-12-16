from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

from utils.serializers import TableSerializer

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://x:1234@localhost:5432/playlists"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


class Base(DeclarativeBase, TableSerializer):
    pass


class Playlists(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, autoincrement=True)
    uid = Column(Integer)
    title = Column(String(255), default='Новый плейлист')
    avatar = Column(String(16), default='default.jpeg')
    description = Column(String(512), default='Новый плейлист')


class Tracks(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pid = Column(Integer)
    tid = Column(Integer)


Base.metadata.create_all(bind=engine)
