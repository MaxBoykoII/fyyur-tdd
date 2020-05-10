from project import db
from project.api.venues.models import Venue
from project.api.misc.crud import get_genres_list
from itertools import groupby
from sqlalchemy import func


def get_venue_by_id(venue_id):
    """
    Get a venue by id

    Paramters:
    ---------
    venue_id (str): id of venue
    """
    return db.session.query(Venue).get(venue_id)


def aggregate_venues():
    """Aggregate venues by state and city"""
    venue_query = db.session.query(Venue).order_by(Venue.state, Venue.city).all()

    groups = [
        (
            *key,
            list(
                [
                    {
                        "id": v.id,
                        "name": v.name,
                        "num_upcoming_shows": len(v.upcoming_shows),
                    }
                    for v in venues
                ]
            ),
        )
        for key, venues in groupby(venue_query, key=lambda v: (v.city, v.state))
    ]

    data = [{"city": g[0], "state": g[1], "venues": g[2]} for g in groups]

    return data


def add_venue(form):
    """
    Create new venue from form data

    Paramters:
    ---------
    form (VenueForm): form containing venue data
    """
    genres = get_genres_list(form.getlist("genres"))

    venue = Venue(
        name=form.get("name"),
        city=form.get("city"),
        state=form.get("state"),
        address=form.get("address"),
        phone=form.get("phone"),
        genres=genres,
        facebook_link=form.get("facebook_link"),
        image_link=form.get("image_link"),
        website=form.get("website"),
        seeking_description=form.get("seeking_description"),
        seeking_talent=True if form.get("seeking_talent") == "y" else False,
    )

    db.session.add(venue)
    db.session.commit()


def update_venue(venue, form):
    """
    Update existing venue using form data

    Paramters:
    ---------
    venue (Venue): venue to be updated
    form (VenueForm): form containing venue data
    """
    genres = get_genres_list(form.getlist("genres"))

    venue.name = form.get("name")
    venue.city = form.get("city")
    venue.state = form.get("state")
    venue.address = form.get("address")
    venue.phone = form.get("phone")
    venue.genres = genres
    venue.facebook_link = form.get("facebook_link")
    venue.image_link = form.get("image_link")
    venue.website = form.get("website")
    venue.seeking_description = form.get("seeking_description")
    venue.seeking_talent = True if form.get("seeking_talent") == "y" else False

    db.session.commit()


def search_venues_by_name(search_term):
    """
    Search for venues by name; results are case insenstive

    Paramters:
    ---------
    search_term (str): partial name of an artist
    """
    if search_term is None or search_term == "":
        return []

    return (
        db.session.query(Venue)
        .filter(func.upper(Venue.name).contains(search_term.upper(), autoescape=True))
        .all()
    )


def delete_venue_by_id(venue_id):
    """
    Delete venue by id

    Paramters:
    ---------
    venue_id (str): id of the venue
    """
    db.session.query(Venue).filter(Venue.id == venue_id).delete()
    db.session.commit()
