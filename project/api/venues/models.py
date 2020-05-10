from project import db
from project.api.misc.models import GenreVenue
from datetime import datetime
from collections import namedtuple


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.relationship("Genre", secondary=GenreVenue, backref="venues")
    website = db.Column(db.String)
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(750))
    shows = db.relationship("Show", back_populates="venue")

    @property
    def genres_list(self):
        genres = [genre.name for genre in self.genres]

        return genres

    @property
    def past_shows(self):
        show_data = [
            show.artist_data for show in self.shows if show.start_time < datetime.now()
        ]

        return show_data

    @property
    def upcoming_shows(self):
        show_data = [
            show.artist_data for show in self.shows if show.start_time >= datetime.now()
        ]

        return show_data

    def as_dict(self):
        data_dict = dict(vars(self))
        data_dict.pop("_sa_instance_state", None)
        data_dict["genres"] = self.genres_list

        return data_dict

    def get_form_data(self):
        data = self.as_dict()
        data.pop("id", None)
        form_data = namedtuple("VenueFormModel", data.keys())(**data)

        return form_data
