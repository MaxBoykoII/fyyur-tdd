from flask import Blueprint, render_template, flash, request
from project.forms import VenueForm
from project.api.venues.crud import get_venue_by_id, aggregate_venues, add_venue
from project import db

venues_blueprint = Blueprint("venues", __name__, template_folder="../templates")


@venues_blueprint.route("/venues/<int:venue_id>")
def show_venue(venue_id):
    venue = get_venue_by_id(venue_id)

    past_shows = venue.past_shows
    upcoming_shows = venue.upcoming_shows

    data = {
        "id": venue.id,
        "name": venue.name,
        "genres": venue.genres_list,
        "address": venue.address,
        "city": venue.city,
        "state": venue.state,
        "phone": venue.phone,
        "website": venue.website,
        "facebook_link": venue.facebook_link,
        "seeking_talent": venue.seeking_talent,
        "seeking_description": venue.seeking_description,
        "image_link": venue.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_venue.html", venue=data)


@venues_blueprint.route("/venues")
def venues():
    data = aggregate_venues()
    return render_template("pages/venues.html", areas=data)


@venues_blueprint.route("/venues/create", methods=["GET"])
def create_venue_form():
    form = VenueForm()
    return render_template("forms/new_venue.html", form=form)


@venues_blueprint.route("/venues/create", methods=["POST"])
def create_venue_submission():
    status_code = 201
    try:
        add_venue(request.form)
        flash("Venue " + request.form["name"] + " was successfully listed!")

    except Exception as err:
        db.session.rollback()

        flash(
            "An error occurred. Venue " + request.form["name"] + " could not be listed."
        )
        print(err)
        status_code = 500

    finally:
        db.session.close()

    return render_template("pages/home.html"), status_code
