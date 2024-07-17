"""
Insta485 following view.

URLs include:
/u/<user_url_slug>/following
"""
import flask
import insta485
from .utils import utils


@insta485.app.route('/u/<user_url_slug>/following/')
@utils.must_be_logged_in('redirect')
@utils.user_must_exist
@insta485.utils.database_query
def show_following(user_url_slug):
    """."""
    users_followed = flask.g.db_cur.execute(
        utils.query_from_sql_file('following.sql'),
        {"username": user_url_slug,
         'logname': flask.session['user']}) or flask.g.db_cur.fetchall()
    for user in users_followed:
        user['relationship'] = utils.user_user_relationship(
            flask.session['user'], user)
    return flask.render_template("following.html",
                                 users_followed=users_followed,
                                 username=user_url_slug)
