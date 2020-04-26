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
