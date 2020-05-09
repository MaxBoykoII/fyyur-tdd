from project import db


class Show(db.Model):
    __tablename__ = "Show"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("Artist.id"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey("Venue.id"), nullable=False)
    start_time = db.Column("start_time", db.DateTime, nullable=False)
    artist = db.relationship("Artist", back_populates="shows")
    venue = db.relation("Venue", back_populates="shows")

    @property
    def artist_data(self):
        artist = {
            "artist_id": self.artist_id,
            "artist_name": self.artist.name,
            "artist_image_link": self.artist.image_link,
            "start_time": self.start_time.isoformat(),
        }

        return artist

    @property
    def venue_data(self):
        venue = {
            "venue_id": self.venue_id,
            "venue_name": self.venue.name,
            "venue_image_link": self.venue.image_link,
            "start_time": self.start_time.isoformat(),
        }

        return venue
