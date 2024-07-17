"""Insta485 accounts endpoint."""
import hashlib
import uuid
import flask
import insta485
from .utils import utils


@insta485.app.route("/accounts/", methods=["POST"])
@utils.endpoint
def accounts():
    """."""
    if flask.request.form['operation'] == 'update_password':
        update_password()
    elif flask.request.form['operation'] == 'edit_account':
        edit_account()
    elif flask.request.form['operation'] == 'delete':
        delete()
    elif flask.request.form['operation'] == 'login':
        login()
    elif flask.request.form['operation'] == 'create':
        create()
    return flask.redirect(flask.url_for("show_index"))


@utils.must_be_logged_in('abort')
@insta485.utils.database_query
@utils.requires_fields('password', 'new_password1', 'new_password2')
def update_password():
    """."""
    verify_password(flask.session['user'],
                    flask.request.form['password'])
    if (flask.request.form['new_password1'] !=
            flask.request.form['new_password2']):
        flask.abort(401)

    hashed_password = hash_password(flask.request.form['new_password1'])
    flask.g.db_cur.execute(
        "UPDATE users "
        "SET password=%(password)s "
        "WHERE username=%(username)s", {
            'username': flask.session['user'],
            'password': hashed_password
        }
    )


@utils.must_be_logged_in('abort')
@insta485.utils.database_query
@utils.requires_fields('email', 'fullname')
def edit_account():
    """."""
    if flask.request.files['file']:
        flask.g.db_cur.execute(
            "SELECT filename FROM users WHERE username=%(username)s",
            {'username': flask.session['user']})
        user_filename = flask.g.db_cur.fetchone()['filename']
        user_filename_path = insta485.app.config['UPLOAD_FOLDER']/user_filename
        user_filename_path.unlink()
        filename = utils.save_file()

        flask.g.db_cur.execute(
            """
            UPDATE users
            SET fullname=%(fullname)s, email=%(email)s, filename=%(file)s
            WHERE username=%(username)s
            """, {
                'username': flask.session['user'],
                'fullname': flask.request.form['fullname'],
                'email': flask.request.form['email'],
                'file': filename
            })
    else:
        flask.g.db_cur.execute(
            "UPDATE users "
            "SET fullname=%(fullname)s, email=%(email)s "
            "WHERE username=%(username)s",
            {'username': flask.session['user'],
             'fullname': flask.request.form['fullname'],
             'email': flask.request.form['email']})


@insta485.utils.database_query
@utils.must_be_logged_in('abort')
def delete():
    """."""
    posts = flask.g.db_cur.execute(
        "SELECT filename FROM posts WHERE owner=%(username)s",
        {'username': flask.session['user']}
    ) or flask.g.db_cur.fetchall()
    user = flask.g.db_cur.execute(
        "SELECT filename FROM users WHERE username=%(username)s",
        {'username': flask.session['user']}
    ) or flask.g.db_cur.fetchone()

    for post in posts:
        (insta485.app.config['UPLOAD_FOLDER']/post['filename']).unlink()
    (insta485.app.config['UPLOAD_FOLDER']/user['filename']).unlink()
    flask.g.db_cur.execute("DELETE FROM users WHERE username=%(username)s", {
        'username': flask.session['user']})
    flask.session.clear()


@insta485.utils.database_query
def verify_password(username, input_password):
    """."""
    user = flask.g.db_cur.execute(
        "SELECT username, password "
        "FROM users "
        "WHERE username = %(username)s ",
        {'username': username}) or flask.g.db_cur.fetchone()
    if not user:
        flask.abort(403)
    # explode password parts
    algorithm, salt, hashed_password = user['password'].split('$')
    # hash input password
    msg = hashlib.new(algorithm)
    msg.update((salt + input_password).encode('utf-8'))
    # check if input password matches password in database
    if msg.hexdigest() != hashed_password:
        flask.abort(403)


@ utils.requires_fields('username', 'password')
def login():
    """."""
    verify_password(flask.request.form['username'],
                    flask.request.form['password'])
    flask.session['user'] = flask.request.form['username']


@insta485.utils.database_query
@ utils.requires_fields('username', 'password', 'fullname', 'email')
@ utils.file_required
def create():
    """."""
    if username_taken():
        flask.abort(409)
    filename = utils.save_file()
    hashed_password = hash_password(flask.request.form['password'])
    # make a connection to the database
    flask.g.db_cur.execute(
        """
        INSERT INTO users
        (username, fullname, email, filename, password)
        VALUES
        (%(username)s, %(fullname)s, %(email)s, %(filename)s, %(password)s)
        """, {
            'username': flask.request.form['username'],
            'fullname': flask.request.form['fullname'],
            'email': flask.request.form['email'],
            'filename': filename,
            'password': hashed_password})

    flask.session['user'] = flask.request.form['username']


def hash_password(input_password):
    """."""
    algorithm = 'sha512'
    salt = uuid.uuid4().hex
    hash_obj = hashlib.new(algorithm)
    password_salted = salt + input_password
    hash_obj.update(password_salted.encode('utf-8'))
    password_hash = hash_obj.hexdigest()
    password_db_string = "$".join([algorithm, salt, password_hash])
    return password_db_string


@insta485.utils.database_query
def username_taken():
    """."""
    flask.g.db_cur.execute(
        """
        SELECT username
        FROM users
        WHERE username = %(username)s
        """,
        {'username': flask.request.form['username']})

    return bool(flask.g.db_cur.fetchone())
