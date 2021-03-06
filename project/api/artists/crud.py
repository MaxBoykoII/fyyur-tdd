from project import db
from project.api.artists.models import Artist
from project.api.misc.crud import get_genres_list
from sqlalchemy import func


def get_artist_list():
    return db.session.query(Artist.id, Artist.name).all()


def add_artist(form):
    """
    Create artist using form data

    Paramters:
    ---------
    form (ArtistForm): form with artist data
    """
    genres = get_genres_list(form.getlist("genres"))
    artist = Artist(
        name=form.get("name"),
        city=form.get("city"),
        state=form.get("state"),
        phone=form.get("phone"),
        genres=genres,
        image_link=form.get("image_link"),
        facebook_link=form.get("facebook_link"),
        website=form.get("website"),
        seeking_venue=True if form.get("seeking_venue") == "y" else False,
        seeking_description=form.get("seeking_description"),
    )

    db.session.add(artist)
    db.session.commit()

    return artist


def get_artist_by_id(artist_id):
    """
    Get an artist by id

    Paramters:
    ---------
    artist_id (str): id of the artist
    """
    return db.session.query(Artist).get(artist_id)


def update_artist(artist, form):
    """
    Update an artist using form data

    Paramters:
    ---------
    artist (Artist): artist to be updated
    form (ArtistForm): form containing updates
    """
    genres = get_genres_list(form.getlist("genres"))

    artist.name = form.get("name")
    artist.city = form.get("city")
    artist.state = form.get("state")
    artist.phone = form.get("phone")
    artist.genres = genres
    artist.image_link = form.get("image_link")
    artist.facebook_link = form.get("facebook_link")
    artist.website = form.get("website")
    artist.seeking_venue = True if form.get("seeking_venue") == "y" else False
    artist.seeking_description = form.get("seeking_description")

    db.session.commit()


def search_artists_by_name(search_term):
    """
    Query db for artists whose names contain
    the given search term; results are case insenstive

    Paramters:
    ---------
    search_term (str): search term for artist name
    """
    if search_term is None or search_term == "":
        return []

    return (
        db.session.query(Artist)
        .filter(func.upper(Artist.name).contains(search_term.upper(), autoescape=True))
        .all()
    )
