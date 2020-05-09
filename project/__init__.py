import os

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
import dateutil.parser
import babel

# instantiate the db
db = SQLAlchemy()


# date time filter
def format_datetime(value, format="medium"):
    date = dateutil.parser.parse(value)
    if format == "full":
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == "medium":
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


# application factory pattern
def create_app(script_info=None):

    # instantiate app
    app = Flask(__name__)

    # register filters
    app.jinja_env.filters["datetime"] = format_datetime

    # set config
    app_settings = os.getenv("APP_SETTINGS")
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    if os.getenv("FLASK_ENV") == "development":
        admin = Admin(template_mode="bootstrap3")
        admin.init_app(app)

        from project.api.artists.models import Artist
        from project.api.venues.models import Venue

        admin.add_view(ModelView(Artist, db.session))
        admin.add_view(ModelView(Venue, db.session))

    # register blueprints
    from project.api.home import home_blueprint
    from project.api.artists.views import artists_blueprint
    from project.api.venues.views import venues_blueprint
    from project.api.shows.views import shows_blueprint
    from project.api.ping import ping_blueprint

    app.register_blueprint(home_blueprint)
    app.register_blueprint(ping_blueprint)
    app.register_blueprint(artists_blueprint)
    app.register_blueprint(venues_blueprint)
    app.register_blueprint(shows_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return {"app": app, "db": db}

    return app
