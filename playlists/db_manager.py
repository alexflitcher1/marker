from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from db import engine, Playlists, Tracks


class DBManagerPlaylists:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def create(self, uid: int, title: str = 'Новый плейлист', avatar: str = 'default.jpg',
               description: str = 'Новый плейлист'):
        playlist = Playlists(
            uid=uid,
            title=title,
            avatar=avatar,
            description=description
        )

        try:
            self.db.add(playlist)
            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return playlist.id

    def update(self, pid: int, title: str = None, description: str = None):
        playlist = self.fetch_id(pid)

        to_update = {
            'title': title if title is not None else playlist.title,
            'description': description if description is not None else playlist.description
        }

        try:
            self.db.query(Playlists) \
                .filter(Playlists.id == pid) \
                .update(to_update)

            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return self.fetch_id(pid)

    def fetch_uid(self, uid: str):
        return self.db.query(Playlists)\
            .filter(Playlists.uid == uid).all()

    def fetch_title(self, title: str):
        return self.db.query(Playlists) \
            .filter(Playlists.title == title).all()

    def fetch_id(self, id: int):
        return self.db.query(Playlists) \
            .filter(Playlists.id == id).first()

    def delete(self, id: int):
        try:
            self.db.query(Playlists) \
                .filter(Playlists.id == id) \
                .delete()

            self.db.commit()
        except exc.SQLAlchemyError:
            return False
        return True


class DBManagerTracks:

    def __init__(self):
        SessionLocal = sessionmaker(autoflush=False, bind=engine)
        self.db = SessionLocal()

    def create(self, pid: int, tid: int):
        track = Tracks(
            pid=pid,
            tid=tid
        )

        try:
            self.db.add(track)
            self.db.commit()
        except exc.SQLAlchemyError:
            return False

        return track.id

    def fetch_tracks(self, pid: int, start: int, stop: int):
        return self.db.query(Tracks) \
            .filter(Tracks.pid == pid) \
            .offset(start) \
            .limit(stop) \
            .all()

    def fetch_track(self, pid: int, tid: int):
        return self.db.query(Tracks) \
            .filter(Tracks.pid == pid, Tracks.tid == tid) \
            .first()

    def delete(self, pid: int, tid: int):
        try:
            self.db.query(Tracks) \
                .filter(Tracks.pid == pid, Tracks.tid == tid) \
                .delete()
        except exc.SQLAlchemyError:
            return False
        return True