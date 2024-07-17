"""Insta485 following endpoint."""
import flask
import insta485
from .utils import utils


@insta485.app.route("/following/", methods=["POST"])
@utils.endpoint
@utils.must_be_logged_in('abort')
def following():
    """."""
    if flask.request.form['operation'] == 'follow':
        follow()
    if flask.request.form['operation'] == 'unfollow':
        unfollow()

    return flask.redirect(flask.url_for("show_index"))


@insta485.utils.database_query
def delete_following(follower, followee):
    """."""
    flask.g.db_cur.execute(
        "DELETE FROM following "
        "WHERE username1=%(username1)s AND username2=%(username2)s",
        {'username1': follower, 'username2': followee}
    )


def unfollow():
    """."""
    if (not user1_follows_user2(flask.session['user'],
                                flask.request.form['username'])):
        flask.abort(409)

    delete_following(flask.session['user'], flask.request.form['username'])


@insta485.utils.database_query
def user1_follows_user2(username1, username2):
    """."""
    user_follows_user = flask.g.db_cur.execute(
        "SELECT * FROM following "
        "WHERE username1=%(username1)s AND username2=%(username2)s",
        {'username1': username1, 'username2': username2}
    ) or flask.g.db_cur.fetchone()

    return bool(user_follows_user)


@insta485.utils.database_query
def create_following(follower, followee):
    """."""
    flask.g.db_cur.execute(
        "INSERT INTO following (username1, username2) "
        "VALUES "
        "(%(username1)s, %(username2)s)",
        {'username1': follower, 'username2': followee}
    )


def follow():
    """."""
    if (user1_follows_user2(flask.session['user'],
                            flask.request.form['username'])):
        flask.abort(409)
    create_following(flask.session['user'], flask.request.form['username'])
