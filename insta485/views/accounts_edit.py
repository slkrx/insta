"""
Insta485 accounts edit view.

URLs include:
/accounts/edit/
"""
import flask
import insta485
from .utils import utils


@insta485.app.route("/accounts/edit/")
@utils.must_be_logged_in('redirect')
@insta485.utils.database_query
def accounts_edit():
    """."""
    user = flask.g.db_cur.execute(
        "SELECT fullname, email, filename, username "
        "FROM users "
        "WHERE username=%(username)s",
        {"username": flask.session['user']}) or flask.g.db_cur.fetchone()
    return flask.render_template('accounts_edit.html', **user)
