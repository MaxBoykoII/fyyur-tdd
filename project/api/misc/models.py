from project import db
from project.api.misc.enums import genres_list


class Genre(db.Model):
    __tablename__ = "Genre"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum(*genres_list, name="genres"), nullable=False, unique=True)


GenreArtist = db.Table(
    "GenreArtist",
    db.Column("artist_id", db.Integer, db.ForeignKey("Artist.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id"), primary_key=True),
)


GenreVenue = db.Table(
    "GenreVenue",
    db.Column("venue_id", db.Integer, db.ForeignKey("Venue.id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("Genre.id"), primary_key=True),
)
