import os

from flask_admin.contrib.sqla import ModelView

from project import db


# Artist Model
class Artist(db.Model):
    __tablename__ = "Artist"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(500))

    @property
    def genres_list(self):
        genres = self.genres.split(",") if self.genres is not None else []

        return genres


if os.getenv("FLASK_ENV") == "development":
    from project import admin

    admin.add_view(ModelView(Artist, db.session))
