"""module for checking requests and redirecting."""
import functools
import uuid
import pathlib
import flask
import insta485


def must_be_logged_in(action):
    """."""
    def outer_wrap(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if 'user' not in flask.session:
                if action == 'redirect':
                    return flask.redirect(flask.url_for('login'))
                flask.abort(403)
            return func(*args, **kwargs)
        return wrapper
    return outer_wrap


def user_exists(username):
    """."""
    insta485.model.get_db()
    flask.g.db_cur.execute("SELECT * FROM users WHERE username=%(username)s",
                           {'username': username})
    return bool(flask.g.db_cur.fetchone())


def user_must_exist(func):
    """."""
    @functools.wraps(func)
    def wrapper(user_url_slug, *args, **kwargs):
        if not user_exists(user_url_slug):
            flask.abort(404)
        return func(user_url_slug, *args, **kwargs)
    return wrapper


def user_user_relationship(logname, user):
    """."""
    if logname == user['username']:
        return ''
    if user['followed_by_current_user']:
        return 'following'
    return 'not following'


def endpoint(func):
    """."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        response = func(*args, **kwargs)
        if 'target' in flask.request.args:
            return flask.redirect(flask.request.args['target'])
        return response
    return wrapper


def query_from_sql_file(filename):
    """."""
    query_file = open(
        insta485.app.config['INSTA485_ROOT'] / 'sql' / filename)
    return query_file.read()


def file_required(func):
    """."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if 'file' not in flask.request.files:
            flask.abort(400)
        if not flask.request.files['file']:
            flask.abort(400)
        return func(*args, **kwargs)
    return wrapper


def save_file():
    """."""
    # Unpack flask object
    fileobj = flask.request.files["file"]
    filename = fileobj.filename

    # Compute base name (filename without directory).  We use a UUID to avoid
    # clashes with existing files, and ensure that the name is compatible with
    # the filesystem.
    uuid_basename = "{stem}{suffix}".format(
        stem=uuid.uuid4().hex,
        suffix=pathlib.Path(filename).suffix
    )

    # Save to disk
    path = insta485.app.config["UPLOAD_FOLDER"]/uuid_basename
    fileobj.save(path)
    return uuid_basename


def postid_img_url_step(self, postid, img_url):
    """."""
    if postid and img_url:
        self.collection.append({'postid': postid, 'img_url': img_url})


def requires_fields(*fields):
    """."""
    def outer_wrapper(func):
        @functools.wraps(func)
        def inner_wrapper(*args, **kwargs):
            if not all(map(lambda field: field in flask.request.form, fields)):
                flask.abort(400)
            if not all(map(
                    lambda field: bool(flask.request.form[field]), fields)):
                flask.abort(400)
            return func(*args, **kwargs)
        return inner_wrapper
    return outer_wrapper
