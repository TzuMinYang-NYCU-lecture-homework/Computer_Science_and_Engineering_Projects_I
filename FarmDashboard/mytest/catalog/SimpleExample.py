import dash
#import dash_core_components as dcc
#import dash_html_components as html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL

import sys
sys.path.append("..")
from db import db

db.connect()
session = db.get_session()
ans = []
field = "demo"
for field_attr in (session.query(db.models.field).all()):
    #field_attr = session.query(db.models.field).filter(db.models.field.name == field) 不知道為什麼不能這樣用，下面的id會有問題
    if field_attr.name == field:
        query_df = (session.query(db.models.field_sensor)
                            .select_from(db.models.field_sensor)
                            .join(db.models.sensor)
                            .filter(db.models.field_sensor.field == field_attr.id)
                            .all())
        for sensor in query_df:
            ans.append(sensor.df_name)

        break

session.close()

for i in ans:
    print(i)

ori_sensor_selects = ["sensor1", "sensor2"]


dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
app = DjangoDash(
    'SimpleExample',
    suppress_callback_exceptions=True, # 忽略callback時遇到id找不到的錯誤
    add_bootstrap_links=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, dbc_css],
)   # replaces dash.Dash

app.layout = dbc.Container(
    [
        dbc.Container([dbc.Row(html.P("")), dbc.Row(html.P("")), dbc.Row(html.P("")), dbc.Row(dbc.Col(html.H2("Visualization"), width=2), justify="center"), dbc.Row(html.P("")), dbc.Row(html.P("")), ]),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            html.P("Step1. Target"), width=3
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(options=["Assess a relationship", "Evaluate a distribution", "Compare data"], value="Assess a relationship", id="select_target"),
                                            width={"size": 6, "offset":1}
                                        )
                                    ]
                                ),
                                dbc.Row(),
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                dbc.Row(dbc.Col(html.P("Recommended Chart Type:"), width={"size": 6}), justify="end"),
                                dbc.Row(dbc.Col(html.P("None", id="Recommended_Chart"), width={"size": 4}), justify="end"),
                            ],
                            width=6,
                        ),
                    ], 
                ),
                dbc.Row(html.P(""))
            ]
            
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
                                        dbc.Col(html.P("Type"), width={'size': 3, 'offset': 1}),
                                        dbc.Col(
                                            dcc.Dropdown(options=["Time Interval", "Realtime"], value="Time Interval"),
                                            width=5
                                        )
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.P("Interval"), width={'size': 3, 'offset': 1}),
                                        dbc.Col(
                                            dcc.Dropdown(options=["second", "minute", "hour", "day", "week"], value="hour", ),
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
                                        dbc.Col(html.P("# of sensors", style={"font-size": "15px"}), width=3, align="center"),
                                        dbc.Col(dbc.Input(value=2, type="number", min=2, max=3, step=1, id='sensor_number_input'), width=3),
                                    ],
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.P("Item"), width={'size': 6, 'offset': 1}),
                                        dbc.Col(html.P("Name"), width=3),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.P('X-axis'), width={'size': 3, 'offset': 1}),
                                        dbc.Col(
                                            dcc.Dropdown(options=["sensor1", "sensor2", "sensor3"], value="sensor1", id={"type": "sensor_select", "index": 0}),
                                            width=4,
                                        ),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(html.P('X-axis'), width={'size': 3, 'offset': 1}),
                                        dbc.Col(
                                            dcc.Dropdown(options=["sensor1", "sensor2", "sensor3"], value="sensor2", id={"type": "sensor_select", "index": 1}),
                                            width=4
                                        ),
                                    ]
                                )
                            ], 
                            id='all_sensor_select',
                            width=6
                        )
                    ]
                ),
            ],
        ),
        dbc.Container(dbc.Row(dbc.Col(dbc.Button("OK", color="primary", size="md"), width=1), justify="center"))
    ],
    style={"font-size": "18px"},
    class_name="dbc"
)

@app.callback(
    Output('all_sensor_select', 'children'),
    Input('sensor_number_input', 'value'),
    State('all_sensor_select', 'children'),
    prevent_initial_call=True
)
def add_all_sensor_select_item(sensor_num, all_sensor_select):
    if sensor_num + 2 > len(all_sensor_select):
        for i in range(sensor_num + 2 - len(all_sensor_select)):
            all_sensor_select.append(
                dbc.Row(
                    [
                        dbc.Col(html.P('X-axis'), width={'size': 3, 'offset': 1}),
                        dbc.Col(
                            dcc.Dropdown(options=["sensor1", "sensor2", "sensor3"], value="sensor3", id={"type": "sensor_select", "index": i + len(all_sensor_select) - 2}),
                            width=4
                        ),
                    ],
                )
            )
            global ori_sensor_selects
            ori_sensor_selects.append("sensor3")

    elif sensor_num + 2 < len(all_sensor_select):
        all_sensor_select = all_sensor_select[0:sensor_num + 2]
        ori_sensor_selects = ori_sensor_selects[0:sensor_num]

    return all_sensor_select

@app.callback(
    Output('sensor_number_input', 'min'),
    Output('sensor_number_input', 'max'),
    Output('sensor_number_input', 'value'),
    Input('select_target', 'value'),
    prevent_initial_call=True
)
def set_sensor_number_input(target):
    if target == "Assess a relationship":
        return 2, 3, 2

    elif target == "Evaluate a distribution":
        return 1, 3, 2
    
    elif target == "Compare data":
        return 1, min(20, len(ans)), 2

@app.callback(
    Output('Recommended_Chart', 'children'),
    Input('select_target', 'value'),
    Input('sensor_number_input', 'value'),
)
def decide_chart_type(target, sensor_num):
    if target == "Assess a relationship":
        if sensor_num == 2:
            return "Scatter Chart"
        elif sensor_num == 3:
            return "Bubble Chart"

    elif target == "Evaluate a distribution":
        if sensor_num == 1:
            return "Column Histogram"
        elif sensor_num == 2:
            return "Scatter Chart"
        elif sensor_num == 3:
            return "3D Scatter Chart"
    
    elif target == "Compare data":
        if sensor_num == 2:
            return "Bar Chart"
        else:
            return "Line Chart"

@app.callback(
    Output({'type': 'sensor_select', 'index': ALL}, 'value'),
    Input({'type': 'sensor_select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def prevent_duplicate_sensor(new_sensor_selects):
    ctx = dash.callback_context
    print(ctx)
    global ori_sensor_selects

    for i in range(len(new_sensor_selects)):
        if ori_sensor_selects[i] != new_sensor_selects[i]:
            changed_id = i
            new_sensor = new_sensor_selects[changed_id]
            old_sensor = ori_sensor_selects[changed_id]
            break

    print(changed_id)
    print(ori_sensor_selects)
        
    for i in range(len(ori_sensor_selects)):
        if new_sensor == ori_sensor_selects[i]:
            ori_sensor_selects[i] = old_sensor
            ori_sensor_selects[changed_id] = new_sensor
            break

    return ori_sensor_selects