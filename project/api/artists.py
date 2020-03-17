from flask import Blueprint, flash, render_template, request

from project import db
from project.api.models import Artist
from project.forms import ArtistForm

artists_blueprint = Blueprint("artists", __name__, template_folder="../templates")


@artists_blueprint.route("/artists", methods=["GET"])
def artists():
    data = db.session.query(Artist.id, Artist.name).all()
    return render_template("pages/artists.html", artists=data)


@artists_blueprint.route("/artists/create", methods=["GET"])
def create_artist_form():
    form = ArtistForm()
    return render_template("forms/new_artist.html", form=form)


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

        db.session.add(artist)
        db.session.commit()

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
