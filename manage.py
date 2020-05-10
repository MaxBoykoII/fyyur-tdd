from flask.cli import FlaskGroup
import datetime
from project import create_app, db
from project.api.misc.models import Genre
from project.api.misc.enums import Genres
from project.api.shows.models import Show
from project.api.artists.models import Artist
from project.api.venues.models import Venue


app = create_app()
cli = FlaskGroup(create_app=create_app)


@cli.command("recreate_db")
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    # Add list of genres
    for name in Genres:
        db.session.add(Genre(name=name.value))
    db.session.commit()

    genres = db.session.query(Genre).all()

    db.session.add(
        Artist(
            name="Guns N Petals",
            city="San Francisco",
            state="CA",
            phone="326-123-5000",
            genres=[genres[0], genres[5]],
            seeking_venue=True,
            seeking_description="Looking for shows to perform at in the San Francisco Bay Area!",
            website="https://www.gunsnpetalsband.com",
            image_link="https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
            facebook_link="https://www.facebook.com/GunsNPetals",
        )
    )

    db.session.add(
        Artist(
            name="Matt Quevedo",
            city="New York",
            state="NY",
            phone="300-400-5000",
            genres=[genres[4], genres[3]],
            image_link="https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
            facebook_link="https://www.facebook.com/mattquevedo923251523",
        )
    )

    db.session.add(
        Venue(
            name="The Musical Hop",
            city="San Francisco",
            state="CA",
            address="1015 Folsom Street",
            genres=[genres[5], genres[2], genres[8]],
            phone="123-123-1234",
            website="https://www.themusicalhop.com",
            image_link="https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            facebook_link="https://www.facebook.com/TheMusicalHop",
            seeking_talent=True,
            seeking_description="We are on the lookout for a local artist to play every two weeks. Please call us.",
        )
    )

    db.session.commit()

    db.session.add(Show(artist_id=1, venue_id=1, start_time=datetime.datetime.now()))

    db.session.commit()


if __name__ == "__main__":
    cli()
