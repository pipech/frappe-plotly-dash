import dash_core_components as dcc
import dash_html_components as html

from frappe import render_template
from jinja2.exceptions import TemplateNotFound


def config_layout(dash_app):
    # dash layout
    dash_app.layout = html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Input(
            id='csrf_token',
            style={'display': 'none'},
        ),
        html.Div(id='page-content'),
    ])

    # get dashboard css from template
    context = {'dashboard_css': ''}
    try:
        context['dashboard_css'] = render_template(
            'templates/dashboard_config.css',
            context={}
        )
    except TemplateNotFound:
        pass

    # Override the underlying HTML template
    html_layout = dash_render_template(
        template_name='templates/dashboard.html',
        context=context,
    )
    dash_app.index_string = html_layout


def dash_render_template(template_name, context={}):
    # default render template by frappe
    template = render_template(template_name, context=context)

    # replacing custom context
    template = template.replace('[%', '{%')
    template = template.replace('%]', '%}')

    return template
