"""REST API for index."""
import flask
import insta485


@insta485.app.route('/api/v1/', methods=['GET'])
def get_index():
    """get_index."""
    return(
        flask.make_response(
            flask.jsonify({
                'posts': '/api/v1/p/',
                'url': '/api/v1/'
            })
        )
    )
