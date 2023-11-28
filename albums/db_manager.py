from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc

from db import engine, Album, Likes


class DBManagerAlbum:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()
    
    def create(self, artist_id: int, title: str,
    description: str, avatar: str, genre: str):
        album = Album(
            artistid=artist_id,
            title=title,
            description=description,
            avatar=avatar,
            genre=genre
        )
        
        try:
            self.db.add(album)
            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return album.id

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
        except exc.SQLAlchemyError:
            return False

        return like.id

    def fetch_likes(self, uid: int):
        return self.db.query(Likes) \
            .filter(Likes.uid == uid) \
            .all()

    def fetch_like(self, uid: int, album_id: int):
        return self.db.query(Likes) \
            .filter(Likes.uid == uid, Likes.albumid == album_id) \
            .first()

    def delete(self, uid: int, album_id: int):
        try:
            self.db.query(Likes) \
                .filter(Likes.uid == uid, Likes.albumid == album_id) \
                .delete()

            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return True
