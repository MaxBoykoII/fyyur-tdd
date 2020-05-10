from project.api.artists.models import Artist
from project.api.misc.enums import Genres
import pytest


def test_get_artists(test_app, test_database):
    client = test_app.test_client()
    resp = client.get("/artists")

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"


def test_get_create_artist_form(test_app):
    client = test_app.test_client()
    resp = client.get("/artists/create")

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"


def test_get_artist(test_app, test_database, template_spy, artist):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.get("/artists/1")

    assert len(template_spy) == 1

    template, context = template_spy[0]

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"

    assert template.name == "pages/show_artist.html"

    view_model = context["artist"]

    assert view_model["id"] == 1
    assert view_model["name"] == artist.name
    assert view_model["city"] == artist.city
    assert view_model["state"] == artist.state
    assert view_model["phone"] == artist.phone
    assert view_model["website"] == artist.website
    assert view_model["genres"] == artist.genres_list
    assert view_model["facebook_link"] == artist.facebook_link
    assert view_model["seeking_venue"] == artist.seeking_venue
    assert view_model["seeking_description"] == artist.seeking_description
    assert view_model["image_link"] == artist.image_link
    assert view_model["past_shows"] == []
    assert view_model["upcoming_shows"] == []
    assert view_model["past_shows_count"] == 0
    assert view_model["upcoming_shows_count"] == 0


def test_add_artist(test_app, test_database, genres):
    artist_data = {
        "name": "Brewmaster",
        "city": "Columbus",
        "state": "OH",
        "phone": "614-399-3453",
        "genres": [Genres.alternative.value],
        "image_link": "www.brewmaster.com/image.png",
        "facebook_link": "www.facebook.com/brewie",
        "website": "www.brewmaster.com",
        "seeking_venue": "y",
        "seeking_description": "Looking for a venue that features Bovine Rhapsody!",
    }

    client = test_app.test_client()
    resp = client.post(
        "/artists/create", data=artist_data, content_type="multipart/form-data"
    )

    assert resp.status_code == 201
    assert resp.content_type == "text/html; charset=utf-8"

    artist = (
        test_database.session.query(Artist)
        .filter(Artist.name == artist_data["name"])
        .first()
    )

    assert artist is not None
    assert artist.city == artist_data["city"]
    assert artist.state == artist_data["state"]
    assert artist.phone == artist_data["phone"]
    assert artist.genres_list == artist_data["genres"]
    assert artist.image_link == artist_data["image_link"]
    assert artist.facebook_link == artist_data["facebook_link"]
    assert artist.website == artist_data["website"]
    assert (
        artist.seeking_venue is True if artist_data["seeking_venue"] == "y" else False
    )
    assert artist.seeking_description == artist_data["seeking_description"]

    test_database.session.delete(artist)
    test_database.session.commit()


def test_edit_artist_get(test_app, test_database, template_spy, artist):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.get("/artists/1/edit")

    assert len(template_spy) == 1

    template, context = template_spy[0]

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"

    assert template.name == "forms/edit_artist.html"

    form_model = context["artist"]

    assert form_model["id"] == artist.id
    assert form_model["name"] == artist.name
    assert form_model["genres"] == artist.genres_list
    assert form_model["city"] == artist.city
    assert form_model["state"] == artist.state
    assert form_model["phone"] == artist.phone
    assert form_model["website"] == artist.website
    assert form_model["facebook_link"] == artist.facebook_link
    assert form_model["seeking_venue"] == artist.seeking_venue
    assert form_model["seeking_description"] == artist.seeking_description
    assert form_model["image_link"] == artist.image_link


def test_edit_artist_post(test_app, test_database, artist):
    artist_id = artist.id
    artist_data = {
        "name": "The Mighty Milk Master",
        "city": "Plain City",
        "state": "OH",
        "phone": "614-399-3453",
        "genres": [Genres.alternative.value, Genres.country.value],
        "image_link": "www.milkmaster.com/image.png",
        "facebook_link": "www.facebook.com/milkmaster",
        "website": "www.milkmaster.com",
        "seeking_venue": "n",
        "seeking_description": "No longer seeking a venue",
    }

    client = test_app.test_client()
    resp = client.post(
        f"/artists/{artist_id}/edit",
        data=artist_data,
        content_type="multipart/form-data",
    )

    assert resp.status_code == 302
    assert resp.content_type == "text/html; charset=utf-8"

    updated_artist = test_database.session.query(Artist).get(artist_id)
    updated_artist_dict = vars(updated_artist)

    for key, value in artist_data.items():
        expected_value = value
        expected_value = value if key != "seeking_venue" else False
        actual_value = (
            updated_artist_dict[key] if key != "genres" else updated_artist.genres_list
        )

        assert actual_value == expected_value


@pytest.mark.parametrize(
    "search_term, results",
    [
        [
            "A",
            {
                "count": 3,
                "data": [
                    {"id": 1, "name": "Guns N Petals", "num_upcoming_shows": 0},
                    {"id": 2, "name": "Matt Quevado", "num_upcoming_shows": 0},
                    {"id": 3, "name": "The Wild Sax Band", "num_upcoming_shows": 0},
                ],
            },
        ],
        [
            "a",
            {
                "count": 3,
                "data": [
                    {"id": 1, "name": "Guns N Petals", "num_upcoming_shows": 0},
                    {"id": 2, "name": "Matt Quevado", "num_upcoming_shows": 0},
                    {"id": 3, "name": "The Wild Sax Band", "num_upcoming_shows": 0},
                ],
            },
        ],
        [
            "band",
            {
                "count": 1,
                "data": [
                    {"id": 3, "name": "The Wild Sax Band", "num_upcoming_shows": 0}
                ],
            },
        ],
        [
            "bAnd",
            {
                "count": 1,
                "data": [
                    {"id": 3, "name": "The Wild Sax Band", "num_upcoming_shows": 0}
                ],
            },
        ],
        ["", {"count": 0, "data": []}],
    ],
)
def test_search_artists(
    test_app, test_database, template_spy, artists, search_term, results
):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.post(
        "/artists/search",
        data={"search_term": search_term},
        content_type="multipart/form-data",
    )

    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"

    assert len(template_spy) == 1

    template, context = template_spy[0]

    assert template.name == "pages/search_artists.html"

    actual_results = context["results"]
    actual_search_term = context["search_term"]

    assert actual_results == results
    assert actual_search_term == search_term
