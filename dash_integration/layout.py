import dash_core_components as dcc
import dash_html_components as html

from frappe import render_template


def config_layout(dash_app):
    # dash layout
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
    ])

    # Override the underlying HTML template
    html_layout = dash_render_template(
        template_name='templates/dashboard.html',
    )
    dash_app.index_string = html_layout


def dash_render_template(template_name):
    # default render template by frappe
    template = render_template(template_name, context={})

    # replacing custom context
    template = template.replace('[%', '{%')
    template = template.replace('%]', '%}')

    return template
