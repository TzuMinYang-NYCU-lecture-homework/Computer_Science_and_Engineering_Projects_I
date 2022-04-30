import dash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
from django_plotly_dash import DjangoDash
from django.conf import settings

settings.configure(DEBUG=True)
app = DjangoDash(
    __name__,
    suppress_callback_exceptions=True,
    add_bootstrap_links=True,
)

app.layout = html.Div(
    [
        dbc.Container(
            [
                dbc.Row(
                        dbc.Col(html.H3("Visualization"), width=2, style={"font-size": "25px"}), className="justify-content-center"
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P("Step1. Target", style={'background-color': 'white'}), width=3
                                    ),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "Assess a relationship", "value": "Assess a relationship"},
                                                {"label": "Evaluate a distribution", "value": "Evaluate a distribution"},
                                                {"label": "Compare data", "value": "Compare data"},
                                            ],
                                            style={'background-color': 'white'}
                                        ),
                                        style={"display": "flex", "flexWrap": "wrap"},
                                        width=5
                                    )
                                ]
                            ),
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.P("Recommended Chart Type:", style={'background-color': 'white'}),
                                html.P("None", id="Recommended_Chart", style={'background-color': 'white'})
                            ],
                            width=6
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.P("Step 2. Time", style={'background-color': 'white'}), width=3),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(width=1),
                                        dbc.Col(
                                        html.P("Type", style={'background-color': 'white'}), width=3
                                        ),
                                        dbc.Col(
                                            dbc.Select(
                                                options=[
                                                    {"label": "Time Interval", "value": "Time Interval"},
                                                    {"label": "Realtime", "value": "Realtime"},
                                                ]
                                            ),
                                            style={"display": "flex", "flexWrap": "wrap"},
                                            width=4
                                        )
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(width=1),
                                        dbc.Col(
                                            html.P("Interval", style={'background-color': 'white'}), width=3
                                        ),
                                        dbc.Col(
                                            dbc.Select(
                                                options=[
                                                    {"label": "second", "value": "second"},
                                                    {"label": "minute", "value": "minute"},
                                                    {"label": "hour", "value": "hour"},
                                                    {"label": "day", "value": "day"},
                                                    {"label": "week", "value": "week"},
                                                ],
                                            ),
                                            style={"display": "flex", "flexWrap": "wrap"},
                                            width=4
                                        )
                                    ]
                                )
                            ],
                            width=6
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(html.P("Step 3. Sensors", style={'background-color': 'white'}), width=4),
                                    dbc.Col(html.P("# of sensors", style={'background-color': 'white', "font-size": "15px"}), width=3),
                                    dbc.Col(dbc.Input(type="number", min=1, max=20, step=1, id='sensor_number_input'), width=2),
                                ],
                            ),
                            width=6
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P("Type", style={'background-color': 'white'}), width=3
                                    ),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "Time Interval", "value": "Time Interval"},
                                                {"label": "Realtime", "value": "Realtime"},
                                            ]
                                        ),
                                        style={"display": "flex", "flexWrap": "wrap"},
                                        width=4
                                    )
                                ]
                            ),
                            width=6
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P("Interval", style={'background-color': 'white'}), width=3
                                    ),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "second", "value": "second"},
                                                {"label": "minute", "value": "minute"},
                                                {"label": "hour", "value": "hour"},
                                                {"label": "day", "value": "day"},
                                                {"label": "week", "value": "week"},
                                            ],
                                        ),
                                        style={"display": "flex", "flexWrap": "wrap"},
                                        width=4
                                    )
                                ]
                            ),
                            width=6
                        )
                    ]
                ),
                dbc.Row(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P("Item", style={'background-color': 'white'}), width=6
                                    ),
                                    dbc.Col(
                                        html.P("Name", style={'background-color': 'white'}), width=3
                                    )
                                ]
                            ),
                            width=5
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P("Delay", style={'background-color': 'white'}), width=5
                                    ),
                                    dbc.Col(
                                        html.P("Resample", style={'background-color': 'white'}), width=3
                                    )
                                ]
                            ),
                            width=6
                        )
                    ]
                ),
            ]
        ),
        dbc.Container([], id='sensor_select'),
        dbc.Container(dbc.Button("OK", color="primary", className="d-grid gap-2 col-1 mx-auto"))
    ],
    style={"font-family": "work sans", "font-size": "20px"},
)

@app.callback(
    Output('sensor_select', 'children'),
    Input('sensor_number_input', 'value'),
    State('sensor_select', 'children'),
    prevent_initial_call=True
)
def add_sensor_select_item(value, children):
    if value > len(children):
        for _ in range(value - len(children)):
            children.append(
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(html.P('X-axis', style={'background-color': 'white'}), width=3),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "Time Interval", "value": "Time Interval"},
                                                {"label": "Realtime", "value": "Realtime"},
                                            ]
                                        ),
                                        width=8
                                    ),
                                ],
                            ),
                            width=4
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(dbc.Input(type="number", min=0, step=1), width=3),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "--", "value": "--"},
                                                {"label": "Second", "value": "Second"},
                                                {"label": "Minute", "value": "Minute"},
                                                {"label": "Hour", "value": "Hour"},
                                                {"label": "Day", "value": "Day"},
                                                {"label": "Week", "value": "Week"},
                                                {"label": "Month", "value": "Month"},
                                            ]
                                        ),
                                        width=4
                                    ),
                                ],
                            ),
                            width=4
                        ),
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "Average", "value": "Average"},
                                                {"label": "Max", "value": "Max"},
                                                {"label": "Min", "value": "Min"},
                                            ]
                                        ),
                                        width=4
                                    ),
                                ],
                            ),
                            width=4
                        ),
                    ]
                )
            )
    elif value < len(children):
        children = children[0:value]

    return children


if __name__ == "__main__":
    pass