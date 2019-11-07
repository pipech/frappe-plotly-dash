import dash
import json

from flask import Flask
from werkzeug.wrappers import Response


# load dash application
server = Flask(__name__)
dash_app = dash.Dash(
    __name__,
    server=server,
    url_base_pathname='/dash/'
)

# config
dash_app.config.suppress_callback_exceptions = True

# registered dash config
with server.app_context():
    # router
    from dash_integration.router import callback
    callback()

    # layout
    from dash_integration.layout import config_layout
    config_layout(dash_app)


def dash_dispatcher(request):
    params = {
        'data': request.data,
        'method': request.method,
        'content_type': request.content_type
    }

    # todo: check test_request_context function
    with server.test_request_context(request.path, **params):
        server.preprocess_request()
        try:
            response = server.full_dispatch_request()
        except Exception as e:
            response = server.make_response(server.handle_exception(e))
        return response.get_data()


def build_ajax(request):
    response = Response()

    data = dash_dispatcher(request)
    if isinstance(data, dict):
        data = json.dumps(data)
    response.data = data

    response.status_code = 200
    response.mimetype = 'application/json'
    response.charset = 'utf-8'

    return response


def build_page(request):
    response = Response()

    data = dash_dispatcher(request)
    response.data = data

    response.status_code = 200
    response.mimetype = 'text/html'
    response.charset = 'utf-8'

    return response
