"""Insta485 comments endpoint."""
import flask
import insta485
from .utils import utils


@insta485.app.route("/comments/", methods=["POST"])
@utils.must_be_logged_in('abort')
@utils.endpoint
def comments():
    """."""
    if flask.request.form['operation'] == 'create':
        create()
    elif flask.request.form['operation'] == 'delete':
        delete()
    return flask.redirect(flask.url_for("show_index"))


@insta485.utils.database_query
def delete_comment(commentid):
    """."""
    flask.g.db_cur.execute(
        "DELETE FROM comments WHERE commentid=%(commentid)s",
        {'commentid': commentid}
    )


def delete():
    """."""
    if (not user_owns_comment(flask.session['user'],
                              flask.request.form['commentid'])):
        flask.abort(403)
    delete_comment(flask.request.form['commentid'])


@insta485.utils.database_query
def user_owns_comment(username, commentid):
    """."""
    comment = flask.g.db_cur.execute(
        "SELECT * FROM comments WHERE commentid=%(commentid)s",
        {'commentid': commentid}) or flask.g.db_cur.fetchone()
    return comment['owner'] == username


@insta485.utils.database_query
def create_comment(postid, text, username):
    """."""
    flask.g.db_cur.execute(
        "INSERT INTO comments "
        "(postid, text, owner) "
        "VALUES (%(postid)s, %(text)s, %(username)s)",
        {'postid': int(postid), 'text': text, 'username': username}
    )


def create():
    """."""
    if not flask.request.form['text']:
        flask.abort(400)
    create_comment(
        flask.request.form['postid'],
        flask.request.form['text'],
        flask.session['user']
    )
