"""REST API for posts."""
import flask
import insta485
from .utils import utils


@insta485.app.route('/api/v1/p/<int:postid>/likes/', methods=["POST"])
@utils.require_login
@insta485.utils.database_query
@utils.require_post_existance
def create_like(postid):
    """create_like."""
    like_exists = bool(flask.g.db_cur.execute(
        "SELECT EXISTS( "
        "   SELECT 1 FROM likes "
        "   WHERE postid=%(postid)s AND owner=%(username)s "
        ") AS like_exists",
        {
            'postid': postid,
            'username': flask.session['user']
        }
    ) or flask.g.db_cur.fetchone()['like_exists'])
    if like_exists:
        return(
            flask.jsonify(
                logname=flask.session['user'],
                message="Confilct",
                postid=postid,
                status_code=409
            ), 409
        )

    flask.g.db_cur.execute(
        "INSERT INTO likes (owner, postid) "
        "VALUES (%(owner)s, %(postid)s)",
        {
            'owner': flask.session['user'],
            'postid': postid
        }
    )
    return(
        flask.jsonify(
            logname=flask.session['user'],
            postid=postid
        ), 201
    )


@insta485.app.route('/api/v1/p/<int:postid>/likes/', methods=["DELETE"])
@utils.require_login
@insta485.utils.database_query
@utils.require_post_existance
def delete_like(postid):
    """delete_like."""
    flask.g.db_cur.execute(
        """
        DELETE FROM likes
        WHERE postid=%(postid)s
        AND owner=%(username)s
        """,
        {
            "postid": int(postid),
            "username": flask.session['user']
        }
    )
    return '', 204


@insta485.app.route('/api/v1/p/<int:postid>/likes/', methods=["GET"])
@utils.require_login
@insta485.utils.database_query
@utils.require_post_existance
def get_likes(postid):
    """get_likes."""
    flask.g.db_cur.execute(
        """
        SELECT a.*, b.* FROM
            (SELECT
            P.postid,
            '/api/v1/p/' || P.postid || '/likes/' AS url,
            COUNT(L.postid) likes_count
            FROM posts P
            LEFT JOIN likes L USING(postid)
            WHERE postid=%(postid)s
            GROUP BY postid
            ) a,
            (SELECT CASE WHEN %(username)s IN
                (SELECT L.owner
                FROM posts P LEFT JOIN likes L USING(postid)
                WHERE postid=%(postid)s)
            THEN 1 ELSE 0 END
            AS logname_likes_this) b
        """,
        {
            'postid': postid,
            'username': flask.session['user']
        }
    )
    likes = flask.g.db_cur.fetchone()

    return flask.jsonify(likes)


@insta485.app.route('/api/v1/p/<int:postid>/comments/', methods=["POST"])
@utils.require_login
@insta485.utils.database_query
@utils.require_post_existance
def create_comment(postid):
    """create_comment."""
    flask.g.db_cur.execute(
        """
        INSERT INTO comments
        (owner, postid, text)
        VALUES (%(owner)s, %(postid)s, %(text)s)
        RETURNING commentid
        """,
        {
            'owner': flask.session['user'],
            'postid': postid,
            'text': flask.request.json['text']
        }
    )
    commentid = flask.g.db_cur.fetchone()['commentid']

    return flask.make_response(flask.jsonify(
        commentid=commentid,
        owner=flask.session['user'],
        owner_show_url="/u/{}/".format(flask.session['user']),
        postid=postid,
        text=flask.request.json['text']
    ), 201)


@insta485.app.route('/api/v1/p/<int:postid>/comments/', methods=["GET"])
@utils.require_login
@insta485.utils.database_query
@utils.require_post_existance
def get_comments(postid):
    """get_comments."""
    comments = flask.g.db_cur.execute(
        "SELECT C.commentid, "
        "C.owner, "
        "'/u/' || C.owner || '/' AS owner_show_url, "
        "P.postid, "
        "C.text "
        "FROM "
        "comments C "
        "JOIN posts P USING(postid) "
        "WHERE P.postid = %(postid)s ",
        {'postid': postid}
    ) or flask.g.db_cur.fetchall()

    return flask.jsonify(comments=comments, url="/api/v1/p/3/comments/")


@insta485.app.route('/api/v1/p/', methods=["GET"])
@utils.require_login
@insta485.utils.database_query
def get_posts():
    """get_posts."""
    size = flask.request.args.get("size", default=10, type=int)
    page = flask.request.args.get("page", default=0, type=int)

    query = ("SELECT postid "
             "FROM posts "
             "WHERE owner IN ( "
             "SELECT username2 "
             "FROM following "
             "WHERE username1 = %(username)s "
             ") "
             "OR owner = %(username)s "
             "ORDER BY postid DESC "
             "LIMIT %(row_count)s OFFSET %(offset)s ")
    query_parameters = {
        'username': flask.session['user'],
        'row_count': size,
        'offset': page * size
    }

    flask.g.db_cur.execute(query, query_parameters)
    postids = flask.g.db_cur.fetchall()

    query_parameters['offset'] += size
    flask.g.db_cur.execute(query, query_parameters)
    if bool(flask.g.db_cur.fetchone()):
        next_page_url = flask.url_for('get_posts', size=size, page=page + 1)
    else:
        next_page_url = ''
    posts = list(
        map(
            lambda postid: {"url": flask.url_for(
                'get_post', postid=postid['postid']), **postid},
            postids
        )
    )
    return flask.jsonify(next=next_page_url, results=posts, url="/api/v1/p/")


@insta485.app.route('/api/v1/p/<int:postid>/', methods=["GET"])
@insta485.utils.database_query
@utils.require_login
@utils.require_post_existance
def get_post(postid):
    """Return post on postid."""
    flask.g.db_cur.execute(
        "SELECT P.created AS age, "
        "'/uploads/' || P.filename AS img_url, "
        "P.owner, "
        "'/uploads/' || U.filename AS owner_img_url, "
        "'/u/' || U.username || '/' AS owner_show_url, "
        "'/p/' || P.postid || '/' AS post_show_url, "
        "'/api/v1/p/3/' || P.postid || '/' AS url "
        "FROM posts P "
        "JOIN users U ON P.owner = U.username "
        "WHERE P.postid = %(postid)s ",
        {'postid': postid}
    )
    post = flask.g.db_cur.fetchone()

    return flask.jsonify(post)
