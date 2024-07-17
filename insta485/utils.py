"""utils."""

import functools
import flask
import insta485

bp = flask.Blueprint('utils', __name__)


def database_query(query):
    """database_query."""
    @functools.wraps(query)
    def wrapper(*args, **kwargs):
        insta485.model.get_db()
        return query(*args, **kwargs)
    return wrapper
