import dash
import dash_core_components as dcc
import dash_html_components as html
import os
import logging

from werkzeug.wsgi import DispatcherMiddleware
from werkzeug.contrib.profiler import ProfilerMiddleware
from werkzeug.wsgi import SharedDataMiddleware
from werkzeug.serving import run_simple

from frappe.app import application
from frappe.middlewares import StaticDataMiddleware


# load dash application
dash_app = dash.Dash(
    __name__,
    requests_pathname_prefix='/dash/',
)

# config
dash_app.config.suppress_callback_exceptions = True

# dash layout
dash_app.layout = html.Div([
    html.H1('HELLO WORLD FROM DASH'),
])

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
