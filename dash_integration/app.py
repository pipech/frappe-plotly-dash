import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import logging
import frappe
import flask
import requests
import urllib

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.contrib.profiler import ProfilerMiddleware
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.serving import run_simple

from frappe.app import application
from frappe.middlewares import StaticDataMiddleware


def dash_render_template(template_name):
    # default render template by frappe
    template = frappe.render_template(template_name, context={})

    # replacing custom context
    template = template.replace('[%', '{%')
    template = template.replace('%]', '%}')

    return template


# load dash application
flask_server = flask.Flask(__name__)
dash_app = dash.Dash(
    __name__,
    server=flask_server,
)

# config
dash_app.config.suppress_callback_exceptions = True
dash_app.config.update({
    'requests_pathname_prefix': '/dash/'
})

# Override the underlying HTML template
html_layout = dash_render_template(
    template_name='templates/dashboard.html',
)
dash_app.index_string = html_layout

# dash layout
dash_app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])


# router for dash app
@dash_app.callback(
    dash.dependencies.Output('page-content', 'children'),
    [
        dash.dependencies.Input('url', 'pathname'),
        dash.dependencies.Input('url', 'href'),
    ]
)
def display_page(pathname, href):
    from dash_integration.dashboard import simple_dash
    from dash_integration.dashboard import simple_dash2

    # extract information from url
    parsed_uri = urllib.parse.urlparse(href)
    url_param = urllib.parse.parse_qs(parsed_uri.query)
    sid = url_param.get('sid', '')
    domain = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)

    # prepare for api
    get_user_info_api = '/api/method/frappe.realtime.get_user_info'
    get_user_info_api_url = '{}{}'.format(domain, get_user_info_api)
    user_param = {'sid': sid}

    # call api
    response = requests.get(
        get_user_info_api_url,
        params=user_param
    )
    if response.status_code == 200:
        user = response.json()['message'].get('user', '')
        print(user)

    # # test frappe connection
    # frappe.connect('site1.local')
    # print(frappe.get_doc('Company', 'SpaceCode'))

    if user == 'Administrator':
        if pathname == '/dash/page-1':
            return simple_dash.layout
        elif pathname == '/dash/page-2':
            return simple_dash2.layout
        else:
            return '404'
    else:
        return '404'


# attach dash to frappe
application = DispatcherMiddleware(application, {
    '/dash': dash_app.server,
})


# custom "serve" command to run frappe with dash
# modified from frappe.app
def serve(application=application, port=8000, profile=False, no_reload=False, no_threading=False, sites_path='.'):
    if profile:
        application = ProfilerMiddleware(
            application,
            sort_by=('cumtime', 'calls')
        )

    if not os.environ.get('NO_STATICS'):
        application = SharedDataMiddleware(application, {
            str('/assets'): str(os.path.join(sites_path, 'assets'))
        })

        application = StaticDataMiddleware(application, {
            str('/files'): str(os.path.abspath(sites_path))
        })

    application.debug = True
    application.config = {
        'SERVER_NAME': 'localhost:8000'
    }

    in_test_env = os.environ.get('CI')
    if in_test_env:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    run_simple(
        '0.0.0.0',
        int(port),
        application,
        use_reloader=False if in_test_env else not no_reload,
        use_debugger=not in_test_env,
        use_evalex=not in_test_env,
        threaded=not no_threading
    )
