import pytest
from flask import template_rendered

from project import create_app, db
from project.api.artists.models import Artist
from project.api.venues.models import Venue


@pytest.fixture(scope="module")
def test_app():
    app = create_app()
    app.config.from_object("project.config.TestingConfig")
    with app.app_context():
        yield app


@pytest.fixture()
def test_database():
    db.create_all()
    yield db
    db.session.remove()
    db.drop_all()


@pytest.fixture
def template_spy(test_app):
    calls = []

    def spy(sender, template, context, **extra):
        calls.append((template, context))

    template_rendered.connect(spy, test_app)

    yield calls

    template_rendered.disconnect(spy, test_app)


@pytest.fixture
def artist(test_database):
    artist = Artist(
        name="Brewmaster",
        city="Columbus",
        state="OH",
        phone="614-399-3453",
        genres="Bovine Rhapsody",
        image_link="www.brewmaster.com/image.png",
        facebook_link="www.facebook.com/brewie",
        seeking_venue=True,
        seeking_description="Looking to rock the barn!",
    )

    db = test_database

    db.session.add(artist)
    db.session.commit()

    yield artist

    db.session.delete(artist)
    db.session.commit()


@pytest.fixture
def artists(test_database):
    artist1 = Artist(
        name="Guns N Petals",
        city="Columbus",
        state="OH",
        phone="614-399-3453",
        genres="Bovine Rhapsody",
        image_link="www.brewmaster.com/image.png",
        facebook_link="www.facebook.com/brewie",
        website="www.brewmaster.com",
        seeking_venue=True,
        seeking_description="Seeking a venue without any bovine rhapsodists!",
    )

    artist2 = Artist(
        name="Matt Quevado",
        city="Columbus",
        state="OH",
        phone="614-399-3453",
        genres="Bovine Rhapsody",
        image_link="www.brewmaster.com/image.png",
        facebook_link="www.facebook.com/brewie",
        website="wwww.mattq.com",
        seeking_venue=False,
        seeking_description="No longer seeking a venue!",
    )

    artist3 = Artist(
        name="The Wild Sax Band",
        city="Columbus",
        state="OH",
        phone="614-399-3453",
        genres="Bovine Rhapsody",
        image_link="www.brewmaster.com/image.png",
        facebook_link="www.facebook.com/brewie",
        website="www.wsaxb.com",
        seeking_venue=True,
        seeking_description="Seeking a venue on the West Coast!",
    )

    db = test_database

    db.session.add(artist1)
    db.session.add(artist2)
    db.session.add(artist3)
    db.session.commit()

    yield [artist1, artist2, artist3]

    db.session.delete(artist1)
    db.session.delete(artist2)
    db.session.delete(artist2)
    db.session.commit()


@pytest.fixture
def venue(test_database):
    venue = Venue(
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
    db.session.add(venue)
    db.session.commit()

    yield venue

    db.session.delete(venue)
    db.session.commit()


@pytest.fixture
def venues(test_database):
    venue1 = Venue(
        name="The Musical Hop",
        city="San Francisco",
        state="CA",
        address="1221 Main ST",
        genres="Rock",
        website="www.themusicalhop.com",
        image_link=None,
        facebook_link=None,
        seeking_talent=False,
        seeking_description=None,
    )

    venue2 = Venue(
        name="The Dueling Pianos Bar",
        city="New York",
        state="NY",
        address="6684 South ST",
        genres="Rock",
        website="www.duelingpianosbar.com",
        image_link=None,
        facebook_link=None,
        seeking_talent=False,
        seeking_description=None,
    )

    venue3 = Venue(
        name="Park Square Live Music & Coffee",
        city="San Francisco",
        state="CA",
        address="6684 South ST",
        genres="Rock",
        website="www.parksquaremusic.com",
        image_link=None,
        facebook_link=None,
        seeking_talent=False,
        seeking_description=None,
    )

    db = test_database

    db.session.add(venue1)
    db.session.add(venue2)
    db.session.add(venue3)
    db.session.commit()

    yield [venue1, venue2, venue3]

    db.session.delete(venue1)
    db.session.commit()


@pytest.fixture()
def venue_data():
    venue_data = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1.com",
    }

    venue = Venue(
        id=venue_data["id"],
        name=venue_data["name"],
        genres=",".join(venue_data["genres"]),
        address=venue_data["address"],
        city=venue_data["city"],
        state=venue_data["state"],
        phone=venue_data["phone"],
        website=venue_data["website"],
        facebook_link=venue_data["facebook_link"],
        seeking_talent=venue_data["seeking_talent"],
        seeking_description=venue_data["seeking_description"],
        image_link=venue_data["image_link"],
    )

    return venue, venue_data
