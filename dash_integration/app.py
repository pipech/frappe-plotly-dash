from __future__ import unicode_literals

from dash_integration.dash_application import build_ajax, build_page
from frappe.app import *


local_manager = LocalManager([frappe.local])


@Request.application
def application(request):
    response = None

    try:
        rollback = True

        init_request(request)

        frappe.recorder.record()

        if frappe.local.form_dict.cmd:
            response = frappe.handler.handle()

        # dash router
        # ####################################################
        elif frappe.request.path.startswith("/dash/_dash"):
            response = build_ajax(request)
        elif frappe.request.path.startswith("/dash/"):
            response = build_page(request)
        # ####################################################

        elif frappe.request.path.startswith("/api/"):
            response = frappe.api.handle()

        elif frappe.request.path.startswith('/backups'):
            response = frappe.utils.response.download_backup(request.path)

        elif frappe.request.path.startswith('/private/files/'):
            response = frappe.utils.response.download_private_file(request.path)

        elif frappe.local.request.method in ('GET', 'HEAD', 'POST'):
            response = frappe.website.render.render()

        else:
            raise NotFound

    except HTTPException as e:
        return e

    except frappe.SessionStopped as e:
        response = frappe.utils.response.handle_session_stopped()

    except Exception as e:
        # dash router
        # ####################################################
        if frappe.request.path.startswith("/dash/_dash"):
            response = build_ajax(request)
        # ####################################################
        else:
            response = handle_exception(e)

    else:
        rollback = after_request(rollback)

    finally:
        if frappe.local.request.method in ("POST", "PUT") and frappe.db and rollback:
            frappe.db.rollback()

        # set cookies
        if response and hasattr(frappe.local, 'cookie_manager'):
            frappe.local.cookie_manager.flush_cookies(response=response)

        frappe.recorder.dump()

        frappe.destroy()

    return response


application = local_manager.make_middleware(application)


def serve(port=8000, profile=False, no_reload=False, no_threading=False, site=None, sites_path='.'):
    global application, _site, _sites_path
    _site = site
    _sites_path = sites_path

    from werkzeug.serving import run_simple

    if profile:
        application = ProfilerMiddleware(
            application,
            sort_by=('cumtime', 'calls'),
        )

    if not os.environ.get('NO_STATICS'):
        application = SharedDataMiddleware(
            application,
            {
                str('/assets'): str(os.path.join(sites_path, 'assets')),
            },
        )

        application = StaticDataMiddleware(
            application,
            {
                str('/files'): str(os.path.abspath(sites_path))
            },
        )

    application.debug = True
    application.config = {
        'SERVER_NAME': 'localhost:8000'
    }

    in_test_env = os.environ.get('CI')
    if in_test_env:
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

    run_simple('0.0.0.0', int(port), application,
        use_reloader=False if in_test_env else not no_reload,
        use_debugger=not in_test_env,
        use_evalex=not in_test_env,
        threaded=not no_threading)
