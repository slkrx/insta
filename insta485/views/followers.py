"""
Insta485 followers view.

URLs include:
/u/<user_url_slug>/followers
"""
import flask
import insta485
from .utils import utils


@insta485.app.route('/u/<user_url_slug>/followers/')
@utils.must_be_logged_in('redirect')
@utils.user_must_exist
@insta485.utils.database_query
def show_followers(user_url_slug):
    """."""
    followers = flask.g.db_cur.execute(
        utils.query_from_sql_file('followers.sql'),
        {"username": user_url_slug, 'logname': flask.session['user']}
    ) or flask.g.db_cur.fetchall()
    for user in followers:
        user['relationship'] = utils.user_user_relationship(
            flask.session['user'], user)
    return flask.render_template("followers.html",
                                 followers=followers,
                                 username=user_url_slug)
