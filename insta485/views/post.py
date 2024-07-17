"""
Insta485 post (detail) view.

URLs include:
/p/<postid_url_slug>
"""
import arrow
import flask
import insta485
from .utils import utils


def step(self, commentid, owner, text):
    """."""
    if commentid and owner and text:
        self.collection.append(
            {'commentid': commentid, 'owner': owner, 'text': text})


@insta485.app.route('/p/<postid_url_slug>/')
@insta485.utils.database_query
@utils.must_be_logged_in('redirect')
def show_post(postid_url_slug):
    """."""
    post = flask.g.db_cur.execute("""
        SELECT L.*,
        (
            SELECT
                COALESCE(ARRAY_AGG(
                    JSON_BUILD_OBJECT(
                        'commentid', commentid,
                        'owner', owner,
                        'text', text
                    )
                ), '{}')
            FROM comments
            WHERE postid=%(postid)s
        ) AS comments
        FROM (
            SELECT
                postid,
                U.username AS owner,
                P.created AS timestamp,
                '/uploads/' || P.filename AS img_url,
                '/uploads/' || U.filename AS owner_img_url,
                %(logname)s IN (
                    SELECT owner FROM likes WHERE postid = %(postid)s
                ) liked_by_user,
                COUNT(L.postid) AS likes
            FROM
                posts P
                INNER JOIN users U ON U.username = P.owner
                LEFT JOIN likes L USING(postid)
            WHERE postid = %(postid)s
            GROUP BY P.postid, U.username
        ) L
    """,
                                  {'postid': int(postid_url_slug),
                                   'logname': flask.session['user']}
                                  ) or flask.g.db_cur.fetchone()
    post['timestamp'] = arrow.get(post['timestamp']).humanize()

    return flask.render_template("show_post.html", post=post)
