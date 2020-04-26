import os

from flask_admin.contrib.sqla import ModelView

from project import db


class Venue(db.Model):
    __tablename__ = "Venue"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String)
    website = db.Column(db.String)
    image_link = db.Column(db.String)
    facebook_link = db.Column(db.String)
    seeking_talent = db.Column(db.Boolean, nullable=False, default=False)
    seeking_description = db.Column(db.String(750))

    @property
    def genres_list(self):
        genres = self.genres.split(",") if self.genres is not None else []

        return genres

    @property
    def past_shows(self):
        show_data = []

        return show_data

    @property
    def upcoming_shows(self):
        show_data = []

        return show_data


if os.getenv("FLASK_ENV") == "development":
    from project import admin

    admin.add_view(ModelView(Venue, db.session))
