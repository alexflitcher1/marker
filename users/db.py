from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://x:1234@postgresserver/users"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()

class Users(Base):
    __tablename__ = "user"

