"""
Insta485 accounts update_password view.

URLs include:
/accounts/password/
"""
import flask
import insta485
from .utils import utils


@insta485.app.route("/accounts/password/")
@utils.must_be_logged_in('redirect')
def accounts_password():
    """."""
    return flask.render_template('accounts_password.html')
