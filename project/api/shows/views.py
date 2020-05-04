from flask import Blueprint, render_template
from project.api.shows.crud import get_shows_list

shows_blueprint = Blueprint("shows", __name__, template_folder="../templates")


@shows_blueprint.route("/shows", methods=["GET"])
def shows():
    data = get_shows_list()

    return render_template("pages/shows.html", shows=data)
