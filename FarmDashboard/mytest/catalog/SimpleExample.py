import dash
#import dash_core_components as dcc
#import dash_html_components as html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = DjangoDash(
    'SimpleExample',
    suppress_callback_exceptions=True,
    add_bootstrap_links=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, dbc_css],
)   # replaces dash.Dash

app.layout = dbc.Container(
    [
        dbc.Container(
            dbc.Alert("Hello Bootstrap!", color="success"),
            className="p-5",
        ),
        dbc.Container(
            dbc.Row(
                        dbc.Col(html.H3("Visualization"), width=2), justify="center"
            ),
        ),
        dbc.Container(
            dbc.Row(
                    [
                        dbc.Col(
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.P("Step1. Target"), width=3
                                    ),
                                    dbc.Col(
                                        dbc.Select(
                                            options=[
                                                {"label": "Assess a relationship", "value": "Assess a relationship"},
                                                {"label": "Evaluate a distribution", "value": "Evaluate a distribution"},
                                                {"label": "Compare data", "value": "Compare data"},
                                            ],
                                        ),
                                        width=5
                                    )
                                ]
                            ),
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.P("Recommended Chart Type:"),
                                html.P("None", id="Recommended_Chart")
                            ],
                            width=6
                        )
                    ]
            ),
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.P("Step 2. Time"), width=3),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(width=1),
                                        dbc.Col(
                                        html.P("Type"), width=3
                                        ),
                                        dbc.Col(
                                            dbc.Select(
                                                options=[
                                                    {"label": "Time Interval", "value": "Time Interval"},
                                                    {"label": "Realtime", "value": "Realtime"},
                                                ]
                                            ),
                                            width=4
                                        )
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(width=1),
                                        dbc.Col(
                                            html.P("Interval"), width=3
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
                                            width=4
                                        )
                                    ]
                                )
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(html.P("Step 3. Sensors"), width=4),
                                        dbc.Col(html.P("# of sensors", style={"font-size": "15px"}), width=3, className="align-middle"),
                                        dbc.Col(dbc.Input(type="number", min=1, max=20, step=1, id='sensor_number_input'), width=3),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.P("Item"), width=6),
                                        dbc.Col(html.P("Name"), width=3)
                                    ]
                                ),
                                dbc.Container([], id='sensor_select'),
                            ],
                            width=6
                        )
                    ]
                ),
            ],
        ),
        dbc.Container(dbc.Row(dbc.Button("OK", color="primary", className="d-grid gap-2 col-1 mx-auto")))
    ],
    style={"font-size": "18px"},
    className="dbc"
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
                        dbc.Col(html.P('X-axis'), width=4),
                        dbc.Col(
                            dbc.Select(
                                options=[
                                    {"label": "sensor1", "value": "sensor1"},
                                    {"label": "sensor12", "value": "sensor12"},
                                ]
                            ),
                            width=4
                        ),
                    ],
                )
            )
    elif value < len(children):
        children = children[0:value]

    return children