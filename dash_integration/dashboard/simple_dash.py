import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from dash_integration.app import dash_app


layout = [
    html.Div([
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                },
            },
        )
    ], className='card-body'),
    dcc.Dropdown(
        options=[
            {'label': 'New York City', 'value': 'NYC'},
            {'label': 'Montréal', 'value': 'MTL'},
            {'label': 'San Francisco', 'value': 'SF'},
        ],
        multi=True,
        value="MTL",
    ),
    # div to forceload data
    html.Div(
        [dcc.Input(
            id='forceLoad',
            type='text',
            value='ForceLoad'
        )],
        style={'display': 'none'},
    ),
]
