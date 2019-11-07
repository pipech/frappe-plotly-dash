import dash
import urllib

from dash_integration.dash_application import dash_app
from dash.dependencies import Input, Output


def callback():
    @dash_app.callback(
        Output('page-content', 'children'),
        [
            Input('url', 'pathname'),
            Input('url', 'href'),
        ],
    )
    def display_page(pathname, href):
        from dash_integration.dashboard import simple_dash
        from dash_integration.dashboard import simple_dash2

        if href:
            # extract information from url
            parsed_uri = urllib.parse.urlparse(href)
            url_param = urllib.parse.parse_qs(parsed_uri.query)
            dashboard = url_param.get('dash', '')[0]

            if dashboard == 'Testing 1':
                return simple_dash.get_layout()
            elif dashboard == 'Testing 2':
                return simple_dash2.layout
            else:
                return '404'
