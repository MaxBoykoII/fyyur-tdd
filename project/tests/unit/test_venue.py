def test_as_dict(venue_data):
    venue, data = venue_data

    assert venue.as_dict() == data


def get_form_data(venue_data):
    venue, data = venue_data

    form_data = dict(data)
    form_data.pop("id", None)
    form_data["genres"] = venue.genres_list

    results = vars(venue.get_form_data())

    for key, value in form_data.items():
        assert results[key] == value
