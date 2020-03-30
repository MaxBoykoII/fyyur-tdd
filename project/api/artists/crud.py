from project import db
from project.api.artists.models import Artist


def get_artist_list():
    return db.session.query(Artist.id, Artist.name).all()


def add_artist(artist):
    db.session.add(artist)
    db.session.commit()
    return artist
