from project import db
from project.api.artists.models import Artist


def get_artist_list():
    return db.session.query(Artist.id, Artist.name).all()


def add_artist(artist):
    db.session.add(artist)
    db.session.commit()
    return artist


def get_artist_by_id(artist_id):
    return db.session.query(Artist).filter(Artist.id == artist_id).first()
