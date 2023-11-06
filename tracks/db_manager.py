from sqlalchemy.orm import sessionmaker
from db import engine, Tracks, Likes
from sqlalchemy import cast
from sqlalchemy import Integer, String

SessionLocal = sessionmaker(autoflush=False, bind=engine)
db = SessionLocal()

class DBManagerTracks:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()
    
    def create(self, artist_id: int, title: str,
    avatar: str, path: str, album_id: int, genre: str):
        track = Tracks(
            title=title,
            artistid=artist_id,
            albumid=album_id,
            avatar=avatar,
            path=path,
            genre=genre
        )
        
        try:
            self.db.add(track)
            self.db.commit()

            return track.id
        except:
            return False

    def fetch_album_id(self, album_id: int):
        return self.db.query(Tracks)\
            .filter(Tracks.albumid == album_id)

    def fetch_id(self, id: int):
        return self.db.query(Tracks)\
        .filter(Tracks.id == id).first()

    def fetch_with_artists(self, album_id: int, title: str):
        return self.db.query(Tracks)\
            .filter(cast(Tracks.albumid, Integer) == album_id, cast(Tracks.title, String) == title) \
            .all()

    def fetch_tracks(self, album_id: int):
        return self.db.query(Tracks)\
            .filter(cast(Tracks.albumid, Integer) == album_id) \
            .all()

    def fetch_title(self, title: str):
        return self.db.query(Tracks) \
            .filter(Tracks.title == title)



class DBManagerLikes:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def create(self, uid: int, track_id: int):
        like = Likes(
            uid=uid,
            trackid=track_id
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

    