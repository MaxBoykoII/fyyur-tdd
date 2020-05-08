from project import db
from project.api.shows.models import Show
from project.api.venues.models import Venue
from project.api.artists.models import Artist
import dateutil.parser


def get_shows_list():
    results = (
        db.session.query(
            Show.venue_id,
            Show.artist_id,
            Venue.name.label("venue_name"),
            Artist.name.label("artist_name"),
            Artist.image_link.label("artist_image_link"),
            Show.start_time,
        )
        .join(Venue, Venue.id == Show.venue_id)
        .join(Artist, Artist.id == Show.artist_id)
        .all()
    )

    shows = [result._asdict() for result in results]

    for show in shows:
        show["start_time"] = show["start_time"].isoformat()

    return shows


def add_show(form):
    start_time = dateutil.parser.parse(form.get("start_time"))
    show = Show(
        artist_id=form.get("artist_id"),
        venue_id=form.get("venue_id"),
        start_time=start_time,
    )

    db.session.add(show)
    db.session.commit()

    return show
