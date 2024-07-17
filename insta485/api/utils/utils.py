"""utils."""
import functools
import flask


def require_login(func):
    """require_login."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'user' not in flask.session:
            return(
                flask.make_response(
                    flask.jsonify(
                        message="Forbidden",
                        status_code=403)),
                403)
        return func(*args, **kwargs)
    return wrapper


def require_post_existance(func):
    """require_post_existance."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        flask.g.db_cur.execute(
            "SELECT EXISTS( "
            "   SELECT 1 FROM posts WHERE postid=%(postid)s "
            ") AS post_exists",
            {'postid': kwargs['postid']}
        )
        post_exists = bool(flask.g.db_cur.fetchone()['post_exists'])
        if post_exists:
            return func(*args, **kwargs)
        return(flask.jsonify(
            message='Not Found',
            status_code=404
        ), 404)
    return wrapper
