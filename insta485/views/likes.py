"""Insta485 likes endpoint."""
import flask
import insta485
from .utils import utils


@insta485.app.route("/likes/", methods=["POST"])
@utils.must_be_logged_in('abort')
@utils.endpoint
def likes():
    """."""
    if flask.request.form['operation'] == 'like':
        like()
    elif flask.request.form['operation'] == 'unlike':
        unlike()
    return flask.redirect(flask.url_for("show_index"))


def unlike():
    """."""
    if (not user_likes_post(flask.session['user'],
                            flask.request.form['postid'])):
        flask.abort(409)
    unlike_post(flask.session['user'], flask.request.form['postid'])


@insta485.utils.database_query
def unlike_post(username, postid):
    """."""
    flask.g.db_cur.execute(
        "DELETE FROM likes "
        "WHERE owner=%(username)s AND postid=%(postid)s",
        {'postid': postid, 'username': username}
    )


@insta485.utils.database_query
def user_likes_post(username, postid):
    """."""
    user_likes = flask.g.db_cur.execute("""
        SELECT P.postid
        FROM posts P
        INNER JOIN likes L USING(postid)
        WHERE P.postid=%(postid)s
        AND L.owner=%(username)s
        """, {
        'postid': postid, 'username': username}
    ) or flask.g.db_cur.fetchone()
    return bool(user_likes)


@insta485.utils.database_query
def like_post(username, postid):
    """."""
    flask.g.db_cur.execute(
        "INSERT INTO likes (owner, postid) "
        "VALUES "
        "(%(username)s, %(postid)s)", {
            'postid': postid, 'username': username}
    )


def like():
    """."""
    if user_likes_post(flask.session['user'], flask.request.form['postid']):
        flask.abort(409)
    like_post(flask.session['user'], flask.request.form['postid'])
