import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from dash_integration.app import dash_app


layout = [
    html.Div([
        dcc.Input(id='aaa', value='initial value', type='text'),
        html.Div(id='bbb')
    ], className='card-body'),
]


@dash_app.callback(
    Output(component_id='bbb', component_property='children'),
    [Input(component_id='aaa', component_property='value')]
)
def update_output_div(input_value):
    return 'You\'ve entered "{}"'.format(input_value)
