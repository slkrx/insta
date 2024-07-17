"""
Insta485 download image view.

URLs include:
/uploads/<path:filename>
"""
from pathlib import Path
import flask
import insta485
from .utils import utils


@insta485.app.route('/uploads/<path:filename>')
@utils.must_be_logged_in('abort')
def download_image(filename):
    """."""
    if not Path(insta485.app.config['UPLOAD_FOLDER']/filename).exists():
        flask.abort(404)

    return flask.send_from_directory(insta485.app.config['UPLOAD_FOLDER'],
                                     filename, as_attachment=True)
