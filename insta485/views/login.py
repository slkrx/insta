"""
Insta485 login view.

URLs include:
GET /accounts/login/
POST /accounts/login/
"""
import flask
import insta485


@insta485.app.route("/accounts/login/")
def login():
    """."""
    # if logged in redirect to index
    # can't use the decorator cuz it redirects to login
    if 'user' in flask.session:
        return flask.redirect(flask.url_for('show_index'))
    # if not logged in render login page
    return flask.render_template("login.html")
