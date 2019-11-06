import dash
import dash_core_components as dcc
import dash_html_components as html
import json
import frappe

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

# dash layout
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1('HELLO FROM DASH EMBED'),
    html.Div(id='page-content'),
])


def dash_dispatcher(request):
    params = {
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


def dash_render(frappe_render):
    def render(*args, **kwargs):
        if frappe.request.path.startswith("/dash/_dash"):
            return build_ajax(frappe.request)
        elif frappe.request.path.startswith("/dash/"):
            return build_page(frappe.request)
        else:
            return frappe_render(*args, **kwargs)

    return render
