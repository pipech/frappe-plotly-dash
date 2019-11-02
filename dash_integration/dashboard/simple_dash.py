import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from dash_integration.app import dash_app



def get_layout():
    print('=====================')
    print(dash_app.fp.db.get_value('User', 'Administrator', 'user_type'))
    print('=====================')

    layout = [
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        'Testing Dashboard'
                    ], className='card-header'),
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
                        ),
                    ], className='card-body'),
                ], className='card')
            ], className='col-md-6'),
            html.Div([
                html.Div([
                    html.Div([
                        'Testing Dashboard'
                    ], className='card-header'),
                    html.Div([
                        dcc.Graph(
                            id='example-graph2',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                                'layout': {
                                    'title': 'Dash Data Visualization'
                                },
                            },
                        ),
                    ], className='card-body'),
                ], className='card')
            ], className='col-md-6')
        ], className='row'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        'Testing Dashboard'
                    ], className='card-header'),
                    html.Div([
                        dcc.Graph(
                            id='example-graph3',
                            figure={
                                'data': [
                                    {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                                    {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
                                ],
                                'layout': {
                                    'title': 'Dash Data Visualization'
                                },
                            },
                        ),
                    ], className='card-body'),
                ], className='card')
            ], className='col-md-6'),
        ], className='row')
    ]

    return layout
