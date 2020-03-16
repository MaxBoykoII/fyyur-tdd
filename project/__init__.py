import os

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# instantiate the db
db = SQLAlchemy()

# application factory pattern
def create_app(script_info=None):

    # instantiate app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # set up extensions
    db.init_app(app)

    # set home route
    '''
    @app.route('/')
    def index():
        return render_template('pages/home.html')
    '''

    # register blueprints
    from project.api.home import home_blueprint
    from project.api.ping import ping_blueprint
    app.register_blueprint(home_blueprint)
    app.register_blueprint(ping_blueprint)

    # shell context for flask cli
    @app.shell_context_processor
    def ctx():
        return { 'app': app, 'db': db }
    
    return app