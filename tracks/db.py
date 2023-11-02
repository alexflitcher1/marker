from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://x:1234@localhost:5432/tracks"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Base(DeclarativeBase):
    pass

class Tracks(Base):
    __tablename__ = "track"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(128))
    artistid = Column(String(512))
    albumid = Column(String(128))
    avatar = Column(String(128))
    path = Column(String(128))

class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trackid = Column(Integer)
    uid = Column(Integer)

Base.metadata.create_all(bind=engine)