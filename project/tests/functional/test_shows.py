from project.forms import ShowForm
from project.api.shows.models import Show
import dateutil.parser


def test_get_shows(test_app, show, venue, artist, template_spy):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.get("/shows")

    assert len(template_spy) == 1
    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"

    template, context = template_spy[0]

    assert template.name == "pages/shows.html"

    actual_shows = context["shows"]
    expected_shows = [
        {
            "venue_id": venue.id,
            "artist_id": artist.id,
            "venue_name": venue.name,
            "artist_name": artist.name,
            "artist_image_link": artist.image_link,
            "start_time": show.start_time.isoformat(),
        }
    ]

    assert actual_shows == expected_shows


def test_create_shows(test_app, template_spy):
    assert len(template_spy) == 0

    client = test_app.test_client()
    resp = client.get("/shows/create")

    assert len(template_spy) == 1
    assert resp.status_code == 200
    assert resp.content_type == "text/html; charset=utf-8"

    template, context = template_spy[0]

    assert template.name == "forms/new_show.html"
    assert type(context["form"]) == ShowForm


def test_create_show_submission(test_app, template_spy, test_database, artist, venue):
    assert len(template_spy) == 0

    start_time_str = "2020-05-08 18:16:45"
    start_time = dateutil.parser.parse(start_time_str)
    artist_id = artist.id
    venue_id = venue.id

    show_data = {
        "artist_id": artist_id,
        "venue_id": venue_id,
        "start_time": start_time_str,
    }

    client = test_app.test_client()
    resp = client.post(
        "/shows/create", data=show_data, content_type="multipart/form-data"
    )

    assert len(template_spy) == 1
    assert resp.status_code == 201
    assert resp.content_type == "text/html; charset=utf-8"

    template, _ = template_spy[0]

    assert template.name == "pages/home.html"

    db = test_database

    show = db.session.query(Show).first()

    assert show is not None
    assert show.artist_id == artist_id
    assert show.venue_id == venue_id
    assert show.start_time == start_time

    db.session.delete(show)
    db.session.commit()
