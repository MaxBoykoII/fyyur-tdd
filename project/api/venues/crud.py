from project import db
from project.api.venues.models import Venue
from itertools import groupby


def get_venue_by_id(venue_id):
    return db.session.query(Venue).get(venue_id)


def aggregate_venues():
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
    venue = Venue(
        name=form.get("name"),
        city=form.get("city"),
        state=form.get("state"),
        address=form.get("address"),
        phone=form.get("phone"),
        genres=form.get("genres"),
        facebook_link=form.get("facebook_link"),
        image_link=form.get("image_link"),
        website=form.get("website"),
        seeking_description=form.get("seeking_description"),
        seeking_talent=True if form.get("seeking_talent") == "y" else False,
    )

    db.session.add(venue)
    db.session.commit()


def update_venue(venue, form):
    venue.name = form.get("name")
    venue.city = form.get("city")
    venue.state = form.get("state")
    venue.address = form.get("address")
    venue.phone = form.get("phone")
    venue.genres = form.get("genres")
    venue.facebook_link = form.get("facebook_link")
    venue.image_link = form.get("image_link")
    venue.website = form.get("website")
    venue.seeking_description = form.get("seeking_description")
    venue.seeking_talent = True if form.get("seeking_talent") == "y" else False

    db.session.commit()
