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
