from flask import Blueprint, render_template, request, flash
from project.api.shows.crud import get_shows_list, add_show
from project.forms import ShowForm
from project import db

shows_blueprint = Blueprint("shows", __name__, template_folder="../templates")


@shows_blueprint.route("/shows", methods=["GET"])
def shows():
    data = get_shows_list()

    return render_template("pages/shows.html", shows=data)


@shows_blueprint.route("/shows/create", methods=["GET"])
def create_shows():
    form = ShowForm()
    return render_template("forms/new_show.html", form=form)


@shows_blueprint.route("/shows/create", methods=["POST"])
def create_show_submission():
    status_code = 201
    show_form = request.form

    try:
        add_show(show_form)
        flash("Show was successfully listed!")

    except Exception as err:
        print(err)
        status_code = 500
        db.session.rollback()
        flash("Unable to create show!")

    finally:
        db.session.close()

    return render_template("pages/home.html"), status_code
