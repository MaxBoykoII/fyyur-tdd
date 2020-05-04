from flask.cli import FlaskGroup
import datetime

from project import create_app, db
from project.api.artists.models import Artist
from project.api.venues.models import Venue
from project.api.shows.models import Show


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        Artist(
            name="Jonny Cash",
            city="New York",
            state="NY",
            phone="674-674-674",
            genres="Folk",
            image_link=None,
            facebook_link=None,
        )
    )

    db.session.add(
        Artist(
            name="Bobby Blue Bland",
            city="San Francisco",
            state="CA",
            phone="216-216-216",
            genres="Blues",
            image_link=None,
            facebook_link=None,
        )
    )

    db.session.add(
        Venue(
            name="The Old Barn",
            city="Plain City",
            state="OH",
            address="5147 Barn Blvd",
            genres="Bovine Rhapsody",
            website="www.oldbarnoh.com",
            image_link=None,
            facebook_link=None,
            seeking_talent=True,
            seeking_description="Looking for some Bovine Rhapsodists!",
        )
    )

    db.session.commit()

    db.session.add(Show(artist_id=1, venue_id=1, start_time=datetime.datetime.now()))

    db.session.commit()


if __name__ == "__main__":
    cli()
