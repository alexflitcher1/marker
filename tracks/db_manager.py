from sqlalchemy.orm import sessionmaker
from db import engine, Tracks, Likes
from sqlalchemy import cast
from sqlalchemy import exc
from sqlalchemy import Integer, String


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
        except exc.SQLAlchemyError:
            return False

        return track.id

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
            .filter(Tracks.title == title) \
            .all()

    def fetch_pagination(self, start: int, stop: int):
        return self.db.query(Tracks) \
            .offset(start) \
            .limit(stop) \
            .all()

    def fetch_artist_tracks(self, id: int, start: int, stop: int):
        return self.db.query(Tracks) \
            .filter(Tracks.artistid == str(id)) \
            .offset(start) \
            .limit(stop) \
            .all()

    def search(self, query: str, start: int, stop: int):
        return self.db.query(Tracks) \
            .filter(Tracks.title.like("%{}%".format(query))) \
            .offset(start) \
            .limit(stop) \
            .all()


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
        except exc.SQLAlchemyError:
            return False

        return like.id
    
    def fetch_likes(self, uid: int):
        return self.db.query(Likes) \
            .filter(Likes.uid == uid) \
            .all()

    def fetch_like(self, uid: int, track_id: int):
        return self.db.query(Likes) \
            .filter(Likes.uid == uid, Likes.trackid == track_id) \
            .first()

    def delete(self, uid: int, track_id: int):
        try:
            self.db.query(Likes) \
                .filter(Likes.uid == uid, Likes.trackid == track_id) \
                .delete()

            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return True