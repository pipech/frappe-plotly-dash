from dash_integration.dash_application import dash_app
from dash.dependencies import Input, Output


def callback():
    @dash_app.callback(
        Output(component_id='my-div', component_property='children'),
        [Input(component_id='my-id', component_property='value')]
    )
    def update_output_div(input_value):
        return 'You\'ve entered "{}"'.format(input_value)
