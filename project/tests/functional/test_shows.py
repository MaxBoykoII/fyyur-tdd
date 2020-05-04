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
    print("date type", type(show.start_time))
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
