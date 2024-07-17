"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import insta485
from .utils import utils


@insta485.app.route('/')
@utils.must_be_logged_in('redirect')
def show_index():
    """."""
    return flask.render_template("index.html")
