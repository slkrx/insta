"""
Insta485 user view.

URLs include:
/u/<user_url_slug>/
"""
import flask
import insta485
from .utils import utils


@insta485.utils.database_query
def get_user(user_url_slug):
    """."""
    flask.g.db_cur.execute(
        """
        SELECT
            COUNT(Posts.postid) AS total_posts,
            Users.username,
            Users.fullname,
            %(logname)s IN (
                SELECT username1
                FROM following
                WHERE username2=%(username)s
            ) AS followed_by_current_user,
            (
                SELECT
                COALESCE(ARRAY_AGG(
                    JSON_BUILD_OBJECT(
                        'postid', postid,
                        'filename', '/uploads/' || filename
                    )
                ), '{}')
                FROM posts
                WHERE owner = %(username)s
            ) AS posts,
            (
                SELECT
                COUNT(username2)
                FROM following
                WHERE username1 = %(username)s
            ) AS following,
            (
                SELECT
                COUNT(username1)
                FROM following
                WHERE username2 = %(username)s
            ) AS followers
        FROM users Users LEFT JOIN posts Posts ON Users.username = Posts.owner
        WHERE Users.username = %(username)s
        GROUP BY Users.username
        """, {
            "username": user_url_slug,
            'logname': flask.session['user']
        })
    return flask.g.db_cur.fetchone()


@insta485.app.route('/u/<user_url_slug>/')
@utils.must_be_logged_in('redirect')
@utils.user_must_exist
def show_user(user_url_slug):
    """."""
    user = get_user(user_url_slug)
    user['logname'] = flask.session['user']
    return flask.render_template("show_user.html", **user)
