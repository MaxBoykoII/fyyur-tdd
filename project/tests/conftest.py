import pytest
from flask import template_rendered

from project import create_app, db
from project.api.artists.models import Artist


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
    )

    db = test_database

    db.session.add(artist)
    db.session.commit()

    yield artist

    db.session.delete(artist)
    db.session.commit()
