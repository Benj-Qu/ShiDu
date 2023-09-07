"""REST API for v1."""
import flask
import index


@index.app.route('/api/v1/')
def get_service():
    """Get service for index."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/",
    }
    return flask.jsonify(**context)
