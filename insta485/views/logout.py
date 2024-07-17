"""
Insta485 logout view.

URLs include:
/accounts/logout/
"""
import flask
import insta485
from .utils import utils


@insta485.app.route("/accounts/logout/", methods=["POST"])
@utils.must_be_logged_in('redirect')
def logout():
    """."""
    flask.session.clear()
    return flask.redirect(flask.url_for('login'))
