"""Insta485 posts endpoint."""
import flask
import insta485
from .utils import utils


@insta485.app.route("/posts/", methods=["POST"])
@utils.endpoint
def posts():
    """."""
    if flask.request.form['operation'] == 'create':
        create()
    elif flask.request.form['operation'] == 'delete':
        delete()

    return flask.redirect(flask.url_for(
        "show_user", user_url_slug=flask.session['user']))


@insta485.utils.database_query
def get_post_by_id(postid):
    """."""
    post = flask.g.db_cur.execute(
        "SELECT * FROM posts WHERE postid=%(postid)s",
        {'postid': postid}
    ) or flask.g.db_cur.fetchone()
    return post


@insta485.utils.database_query
@utils.must_be_logged_in('abort')
def delete():
    """."""
    post = get_post_by_id(flask.request.form['postid'])
    if flask.session['user'] != post['owner']:
        flask.abort(403)

    (insta485.app.config['UPLOAD_FOLDER']/post['filename']).unlink()
    flask.g.db_cur.execute("DELETE FROM posts WHERE postid=%(postid)s",
                           {'postid': flask.request.form['postid']})


@insta485.utils.database_query
def create_post(filename, owner):
    """."""
    flask.g.db_cur.execute(
        "INSERT INTO posts (filename, owner) "
        "VALUES (%(filename)s, %(owner)s)",
        {'filename': filename, 'owner': owner}
    )


@utils.file_required
def create():
    """."""
    filename = utils.save_file()
    create_post(filename, flask.session['user'])
