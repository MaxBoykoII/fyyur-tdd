from project.api.misc.models import Genre
from project import db


def get_genres_list(genres):
    results = db.session.query(Genre).filter(Genre.name.in_(genres)).all()

    return results
