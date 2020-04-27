from project.forms import VenueForm
from project.api.venues.models import Venue


def test_get_venue(test_app, test_database, template_spy, venue):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.get("/venues/1")

    assert len(template_spy) == 1

    template, context = template_spy[0]

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"

    assert template.name == "pages/show_venue.html"

    view_model = context["venue"]

    assert view_model["id"] == 1
    assert view_model["name"] == venue.name
    assert view_model["city"] == venue.city
    assert view_model["state"] == venue.state
    assert view_model["phone"] == venue.phone
    assert view_model["website"] == venue.website
    assert view_model["genres"] == venue.genres_list
    assert view_model["facebook_link"] == venue.facebook_link
    assert view_model["seeking_talent"] == venue.seeking_talent
    assert view_model["seeking_description"] == venue.seeking_description
    assert view_model["image_link"] == venue.image_link
    assert view_model["past_shows"] == []
    assert view_model["upcoming_shows"] == []
    assert view_model["past_shows_count"] == 0
    assert view_model["upcoming_shows_count"] == 0


def test_get_venues(test_app, test_database, template_spy, venues):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.get("/venues")

    assert len(template_spy) == 1

    template, context = template_spy[0]

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"

    assert template.name == "pages/venues.html"

    view_model = context["areas"]

    expected_view_model = [
        {
            "city": "San Francisco",
            "state": "CA",
            "venues": [
                {"id": 1, "name": "The Musical Hop", "num_upcoming_shows": 0},
                {
                    "id": 3,
                    "name": "Park Square Live Music & Coffee",
                    "num_upcoming_shows": 0,
                },
            ],
        },
        {
            "city": "New York",
            "state": "NY",
            "venues": [
                {"id": 2, "name": "The Dueling Pianos Bar", "num_upcoming_shows": 0}
            ],
        },
    ]

    assert view_model == expected_view_model


def test_get_create_venue_form(test_app, template_spy):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.get("/venues/create")

    assert len(template_spy) == 1

    template, context = template_spy[0]

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"
    assert template.name == "forms/new_venue.html"
    assert type(context["form"]) == VenueForm


def test_create_venue(test_app, test_database):
    client = test_app.test_client()

    venue_data = {
        "name": "Music By The Bay",
        "city": "San Fransciso",
        "state": "CA",
        "address": "11111 1 St",
        "phone": "(111)-111-111",
        "genres": "Folk, Jazz",
        "website": "www.musicbythebay.com",
        "image_link": "www.musicbythebay.com/img/001",
        "facebook_link": "www.facebook.com/musicbytheby",
        "seeking_talent": "y",
        "seeking_description": "Looking for local musicians who have the goove",
    }

    resp = client.post(
        "/venues/create", data=venue_data, content_type="multipart/form-data"
    )

    assert resp.status_code == 201
    assert resp.content_type == "text/html; charset=utf-8"

    db = test_database

    venue = db.session.query(Venue).filter(Venue.name == venue_data["name"]).first()
    venue_dict = vars(venue)

    for key, value in venue_data.items():
        expected_value = value if key != "seeking_talent" else True
        actual_value = venue_dict[key]
        assert actual_value == expected_value
