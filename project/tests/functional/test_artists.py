from project.api.artists.models import Artist


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
    assert view_model["website"] == "https://www.gunsnpetalsband.com"
    assert view_model["genres"] == artist.genres_list
    assert view_model["facebook_link"] == artist.facebook_link
    assert view_model["seeking_venue"] is True
    assert (
        view_model["seeking_description"]
        == "Looking for shows to perform at in the San Francisco Bay Area!"
    )
    assert view_model["image_link"] == artist.image_link
    assert view_model["past_shows"] == []
    assert view_model["upcoming_shows"] == []
    assert view_model["past_shows_count"] == 0
    assert view_model["upcoming_shows_count"] == 0


def test_add_artist(test_app, test_database):
    artist_data = {
        "name": "Brewmaster",
        "city": "Columbus",
        "state": "OH",
        "phone": "614-399-3453",
        "genres": "Bovine Rhapsody",
        "image_link": "www.brewmaster.com/image.png",
        "facebook_link": "www.facebook.com/brewie",
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
    assert artist.genres == artist_data["genres"]
    assert artist.image_link == artist_data["image_link"]
    assert artist.facebook_link == artist_data["facebook_link"]

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
    assert form_model["website"] == "https://www.gunsnpetalsband.com"
    assert form_model["facebook_link"] == artist.facebook_link
    assert form_model["seeking_venue"] is True
    assert (
        form_model["seeking_description"]
        == "Looking for shows to perform at in the San Francisco Bay Area!"
    )
    assert form_model["image_link"] == artist.image_link


def test_edit_artist_post(test_app, test_database, artist):
    artist_data = {
        "name": "The Mighty Milk Master",
        "city": "Plain City",
        "state": "OH",
        "phone": "614-399-3453",
        "genres": "Alternative",
        "image_link": "www.milkmaster.com/image.png",
        "facebook_link": "www.facebook.com/milkmaster",
    }

    client = test_app.test_client()
    resp = client.post(
        "/artists/1/edit", data=artist_data, content_type="multipart/form-data"
    )

    assert resp.status_code == 302
    assert resp.content_type == "text/html; charset=utf-8"

    updated_artist = test_database.session.query(Artist).get(1)
    updated_artist_dict = vars(updated_artist)

    for key, value in artist_data.items():
        assert value == updated_artist_dict[key]
