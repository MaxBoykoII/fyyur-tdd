from flask import Blueprint, flash, render_template, request, redirect, url_for
from project.forms import ArtistForm
from collections import namedtuple

from project import db
from project.api.artists.models import Artist
from project.api.artists.crud import (
    get_artist_list,
    add_artist,
    get_artist_by_id,
    update_artist,
)

artists_blueprint = Blueprint("artists", __name__, template_folder="../templates")


@artists_blueprint.route("/artists", methods=["GET"])
def artists():
    data = get_artist_list()
    return render_template("pages/artists.html", artists=data)


@artists_blueprint.route("/artists/<int:artist_id>")
def show_artist(artist_id):
    artist = get_artist_by_id(artist_id)

    past_shows = []
    upcoming_shows = []

    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres_list,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": artist.facebook_link,
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template("pages/show_artist.html", artist=data)


@artists_blueprint.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


@artists_blueprint.route("/artists/<int:artist_id>/edit", methods=["GET"])
def edit_artist(artist_id):
    artist = get_artist_by_id(artist_id)
    data = {
        "id": artist.id,
        "name": artist.name,
        "genres": artist.genres_list,
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": artist.facebook_link,
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": artist.image_link,
    }

    form_data = namedtuple("ArtistFormModel", data.keys())(**data)

    form = ArtistForm(obj=form_data)

    return render_template("forms/edit_artist.html", form=form, artist=data)


@artists_blueprint.route("/artists/<int:artist_id>/edit", methods=["POST"])
def edit_artist_submission(artist_id):

    try:
        artist = get_artist_by_id(artist_id)
        update_artist(artist, request.form)

        flash("Artist " + request.form["name"] + " was successfully updated!")

    except Exception as err:
        print(err)
        db.session.rollback()

        flash(
            "An error occurred. Artist "
            + request.form["name"]
            + " could not be updated."
        )

    finally:
        db.session.close()

    return redirect(url_for("artists.show_artist", artist_id=artist_id))


@artists_blueprint.route("/artists/create", methods=["POST"])
def create_artist_submission():
    status_code = 201

    try:
        artist = Artist(
            name=request.form.get("name"),
            city=request.form.get("city"),
            state=request.form.get("state"),
            phone=request.form.get("phone"),
            genres=request.form.get("genres"),
            image_link=request.form.get("image_link"),
            facebook_link=request.form.get("facebook_link"),
        )

        add_artist(artist)

        flash("Artist " + request.form["name"] + " was successfully listed!")

    except Exception as err:
        print(err)
        db.session.rollback()
        status_code = 500

        flash(
            "An error occurred. Artist "
            + request.form["name"]
            + " could not be listed."
        )

    finally:
        db.session.close()

    return render_template("pages/home.html"), status_code
