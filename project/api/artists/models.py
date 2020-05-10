from datetime import datetime
from project import db
from project.api.misc.models import GenreArtist


class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120))
    genres = db.relationship("Genre", secondary=GenreArtist, backref="artists")
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    website = db.Column(db.String)
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(750))
    shows = db.relationship("Show", back_populates="artist")

    @property
    def genres_list(self):
        genres = [genre.name for genre in self.genres]
        return genres

    @property
    def past_shows(self):
        shows = [
            show.venue_data for show in self.shows if show.start_time < datetime.now()
        ]

        return shows

    @property
    def upcoming_shows(self):
        shows = [
            show.venue_data for show in self.shows if show.start_time >= datetime.now()
        ]

        return shows
