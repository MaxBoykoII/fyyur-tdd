from project.api.models import Artist


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
