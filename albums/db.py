from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://x:1234@localhost:5432/albums"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

class Base(DeclarativeBase):
    pass

class Album(Base):
    __tablename__ = "album"

    id = Column(Integer, primary_key=True, autoincrement=True)
    artistid = Column(Integer)
    title = Column(String(255))
    discription = Column(String(512))
    avatar = Column(String(128))
    genre = Column(String(32))

class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    albumid = Column(Integer)
    uid = Column(Integer)

Base.metadata.create_all(bind=engine)