import urllib

from dash_integration.dash_application import dash_app
from dash_integration.auth import has_desk_permission
from dash_integration.auth import has_dashboard_permission
from dash_dashboard.router import dashboard_route
from dash_dashboard.router import dashboard_callback
from dash.dependencies import Input, Output


@dashboard_callback
def callback():
    @dash_app.callback(
        Output('page-content', 'children'),
        [
            Input('url', 'href'),
        ],
    )
    def display_page(href):
        if href:
            # extract information from url
            parsed_uri = urllib.parse.urlparse(href)
            url_param = urllib.parse.parse_qs(parsed_uri.query)
            dashboard = url_param.get('dash', '')[0]

            if has_desk_permission():
                if has_dashboard_permission(dashboard):
                    return dash_route(dashboard)
                else:
                    return 'You are not permitted to access this dashboard'
            else:
                return 'You are not permitted to access this page'


@dashboard_route
def dash_route(dashboard):
    return '404'
