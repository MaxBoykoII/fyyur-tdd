from project.api.misc.models import Genre
from project import db


def get_genres_list(genres):
    """
    Convert list of genre names (strings) to corresponding
    Genre objects

    Paramters:
    ---------
    genres (list[str]): list of genre names
    """
    results = db.session.query(Genre).filter(Genre.name.in_(genres)).all()

    return results
