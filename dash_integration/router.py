import urllib
import dash_core_components as dcc
import dash_html_components as html
import urllib.parse as urlparse
import frappe

from dash_integration.dash_application import dash_app
from dash_integration.auth import has_desk_permission
from dash_integration.auth import has_dashboard_permission
from dash_dashboard.router import dashboard_route
from dash_dashboard.router import dashboard_callback
from dash.dependencies import Input, Output


@dashboard_callback
def callback():
    @dash_app.callback(
        [
            Output('page-content', 'children'),
            Output('csrf_token', 'value'),
        ],
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

            csrf_token = frappe.local.session.data.csrf_token

            if has_desk_permission():
                if has_dashboard_permission(dashboard):
                    return [
                        dash_route(dashboard),
                        csrf_token,
                    ]
                else:
                    return [
                        'You are not permitted to access this dashboard',
                        csrf_token,
                    ]
            else:
                return [
                    get_not_permitted_layout(href),
                    csrf_token,
                ]


@dashboard_route
def dash_route(dashboard):
    return '404'


def get_not_permitted_layout(href):
    parsed = urlparse.urlparse(href)
    layout = html.Div(
        [
            html.Div(
                className='modal-background',
            ),
            html.Div(
                [
                    html.Header(
                        [
                            html.P(
                                'Not Permitted',
                                className='modal-card-title',
                            ),
                            html.Img(
                                src="/assets/dash_dashboard/images/eucerin_logo.svg",
                                style={'height': '24px'},
                            ),
                        ],
                        className='modal-card-head',
                    ),
                    html.Section(
                        [
                            html.P(
                                'You are not permitted to access this page',
                                className='modal-card-title',
                            ),
                        ],
                        className='modal-card-body',
                        style={
                            'border-bottom-right-radius': 0,
                            'border-bottom-left-radius': 0,
                        },
                    ),
                    html.Section(
                        html.A(
                            'Login',
                            href='/dashboard?{}'.format(parsed.query),
                            className='button is-small is-info',
                            style={
                                'background-color': '#83868c',
                            },
                        ),
                        className='modal-card-foot',
                        style={
                            'padding': '12px 16px',
                        },
                    ),
                ],
                className='modal-card',
            )
        ],
        className='modal db-modal is-active',
    )
    return layout
