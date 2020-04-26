from project import db
from project.api.venues.models import Venue


def get_venue_by_id(venue_id):
    return db.session.query(Venue).get(venue_id)
