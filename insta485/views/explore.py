"""
Insta485 explore view.

URLs include:
/u/explore/
"""
import flask
import insta485
from .utils import utils


@insta485.app.route('/explore/')
@utils.must_be_logged_in('redirect')
@insta485.utils.database_query
def show_explore():
    """."""
    users = flask.g.db_cur.execute(
        utils.query_from_sql_file('explore.sql'), {
            'username': flask.session['user']}) or flask.g.db_cur.fetchall()
    for user in users:
        user['relationship'] = utils.user_user_relationship(
            flask.session['user'], user)

    return flask.render_template("explore.html", users=users)
