from sqlalchemy.orm import sessionmaker
from db import engine, Album, Likes

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

class DBManagerAlbum:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()
    
    def create(self, artist_id: int, title: str,
    discription: str, avatar: str):
        album = Album(
            artistid=artist_id,
            title=title,
            discription=discription,
            avatar=avatar
        )
        
        try:
            self.db.add(album)
            self.db.commit()

            return album.id
        except:
            return False

    def fetch_artist_id(self, artist_id: int):
        return self.db.query(Album)\
        .filter(Album.artistid == artist_id)

    def fetch_id(self, id: int):
        return self.db.query(Album)\
        .filter(Album.id == id).first()

    def fetch_title(self, title: str):
        return self.db.query(Album) \
        .filter(Album.title == title)



class DBManagerLikes:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def create(self, uid: int, album_id: int):
        like = Likes(
            uid=uid,
            albumid=album_id
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

