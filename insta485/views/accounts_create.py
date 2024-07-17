"""
Insta485 accounts create view.

URLs include:
/accounts/create/
"""
import flask
import insta485


@insta485.app.route("/accounts/create/")
def accounts_create():
    """."""
    if 'user' in flask.session:
        return flask.redirect(flask.url_for('accounts_edit'))
    return flask.render_template('accounts_create.html')
