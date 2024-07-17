"""
Insta485 accounts delete view.

URLs include:
/accounts/delete/
"""
import flask
import insta485
from .utils import utils


@insta485.app.route("/accounts/delete/")
@utils.must_be_logged_in('redirect')
def accounts_delete():
    """."""
    return flask.render_template('accounts_delete.html')
