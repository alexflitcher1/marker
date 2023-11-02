from sqlalchemy.orm import sessionmaker
from db import engine, Artist, Likes

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()


class DBManagerArtist:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()
    
    def create(self, name: str, description: str,
               avatar: str, background: str):

        artist = Artist(
            name=name,
            discription=description,
            avatar=avatar,
            background=background
        )
        
        try:
            self.db.add(artist)
            self.db.commit()

            return artist.id
        except:
            return False

    def fetch_id(self, artist_id: int):
        return self.db.query(Artist)\
            .filter(Artist.id == artist_id).first()

    def fetch_title(self, name: str):
        return self.db.query(Artist) \
            .filter(Artist.name == name)


class DBManagerLikes:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def create(self, uid: int, artist_id: int):
        like = Likes(
            uid=uid,
            artistid=artist_id,
        )
        
        try:
            self.db.add(like)
            self.db.commit()

            return like.id
        except:
            return False

    def fetch_likes(self, uid: int):
        return self.db.query(Likes) \
            .filter(Likes.uid == uid) \
            .all()
