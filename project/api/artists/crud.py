from project import db
from project.api.artists.models import Artist
from sqlalchemy import func


def get_artist_list():
    return db.session.query(Artist.id, Artist.name).all()


def add_artist(artist):
    db.session.add(artist)
    db.session.commit()
    return artist


def get_artist_by_id(artist_id):
    return db.session.query(Artist).get(artist_id)


def update_artist(artist, form):
    artist.name = form.get("name")
    artist.city = form.get("city")
    artist.state = form.get("state")
    artist.phone = form.get("phone")
    artist.genres = form.get("genres")
    artist.image_link = form.get("image_link")
    artist.facebook_link = form.get("facebook_link")

    db.session.commit()


def search_artists_by_name(search_term):
    if search_term is None or search_term == "":
        return []
    return (
        db.session.query(Artist)
        .filter(func.upper(Artist.name).contains(search_term.upper(), autoescape=True))
        .all()
    )
