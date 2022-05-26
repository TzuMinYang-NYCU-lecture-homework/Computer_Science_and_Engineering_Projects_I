import dash
#import dash_core_components as dcc
#import dash_html_components as html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import datetime
import json

# for graph
import plotly.express as px
import plotly.graph_objects as go # for 3d
import numpy as np # for 3d
import pandas as pd
from plotly.validators.scatter.marker import SymbolValidator

# for db
import sys
sys.path.append("..")
from db import db

"""
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
"""
chart_to_item_map = {
    "Scatter Chart": ["X-axis", "Y-axis"], 
    "Bubble Chart": ["X-axis", "Y-axis", "Radius"], 
    "Column Histogram": ["X-axis"], 
    "3D Scatter Chart": ["X-axis", "Y-axis", "Z-axis"], 
    "Bar Chart": ["Red", "Orange"], 
    #"Line Chart": ["Blue", "Red", "Green", "Purple", "Orange", "Sky blue", "Mgenta", "Grass green", "Pink", "Yello"] #!!! 要20個 , 
    "Line Chart": ["Circle", "Square", "Diamond", "Cross", "X", "Triangle-up", "Triangle-down", "Triangle-left", "Triangle-right", "Triangle-ne", "Triangle-se", "Triangle-sw", "Triangle-nw", "Pentagon", "Hexagon", "Hexagon2", "Octagon", "Star", "Hexagram", "Star-trigangle-up"] #!!! 要20個 
}

sensor_num_to_chart_map = {
    1: ["Column Histogram", "Bar Chart", "Line Chart"],
    2: ["Scatter Chart", "Bar Chart", "Line Chart"],
    3: ["Bubble Chart", "3D Scatter Chart", "Line Chart"],
    4: ["Line Chart"],
    5: ["Line Chart"],
    6: ["Line Chart"],
    7: ["Line Chart"],
    8: ["Line Chart"],
    9: ["Line Chart"],
    10: ["Line Chart"],
    11: ["Line Chart"],
    12: ["Line Chart"],
    13: ["Line Chart"],
    14: ["Line Chart"],
    15: ["Line Chart"],
    16: ["Line Chart"],
    17: ["Line Chart"],
    18: ["Line Chart"],
    19: ["Line Chart"],
    20: ["Line Chart"],
}

#dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css"
#work_sans_regular_css = "https://fonts.googleapis.com/css2?family=Work+Sans&display=swap"
#work_sans_regular_and_semibold_css = "https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600&display=swap"
#work_sans_regular_and_medium_css = "https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;500&display=swap"
#work_sans_light_and_medium_css = "https://fonts.googleapis.com/css2?family=Work+Sans:wght@300;500&display=swap"
work_sans_regular_and_medium_and_black_css = "https://fonts.googleapis.com/css2?family=Work+Sans:wght@400;600;900&display=swap"
app = DjangoDash(
    'SimpleExample',
    suppress_callback_exceptions=True, # 忽略callback時遇到id找不到的錯誤
    add_bootstrap_links=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP, work_sans_regular_and_medium_and_black_css],
)   # replaces dash.Dash

app.layout = dbc.Container(#, "border-width": "3px", "border-style": "solid"
    [
        dcc.Interval(id="plot_interval", interval=5000, disabled=True),
        dcc.Store(id='realtime_start_time'),
        dcc.Store(id='field_sensor'),
        dcc.Store(id='field_name'),
        dcc.Location(id='url', refresh=False),
        dbc.Container([dbc.Row(html.P("")), dbc.Row(dbc.Col("Visualization", width=12), justify="center", style={"font-size": "40px", "font-weight": "600", "color": "rgb(255, 255, 255)", "text-align": "center", "background-color": "rgb(41, 105, 176, 0.7)", "border-radius": "10px"}), dbc.Row(html.P("")), dbc.Row(html.P("")), ]),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Font("Step 1. ", style={"color": "#999"}),
                                                "Target"
                                            ],
                                            width=4,
                                            style={"font-weight": "600"},
                                            align="center"
                                        ),
                                        dbc.Col(
                                            dcc.Dropdown(options=["Assess a relationship", "Evaluate a distribution", "Compare data"], value="Assess a relationship", id="select_target"),
                                            width={"size": 6},
                                            align="center"
                                        )
                                    ]
                                ),
                                dbc.Row(),
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                #dbc.Row(dbc.Col(html.P("Recommended Chart Type:"), width={"size": 6}), justify="end"), #!!! Col要設定width, justify才會起作用，不知道原因
                                #dbc.Row(dbc.Col(html.P("None", id="Recommended_Chart"), width={"size": 4}), justify="end"),
                                dbc.Row(
                                    dbc.Col(
                                        [
                                            html.Font("Recommended Chart Type: ", style={"color": "#999"}),
                                            "None"
                                        ], 
                                        id="Recommended_Chart",
                                        className="text-right", 
                                        width={"size": 8}, 
                                        align="center"
                                    ),
                                    justify="end",
                                    style={"font-size": "15px"}
                                ), #!!! Col要設定width, justify才會起作用，不知道原因
                            ],
                            width=6,
                        ),
                    ], 
                ),
                dbc.Row(html.P("")),
            ]
            
        ),
        dbc.Container(
            [
                dbc.Row(html.P("")),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Font("Step 2. ", style={"color": "#999"}),
                                                "Time"
                                            ],
                                            width=4,
                                            style={"font-weight": "600"},
                                            align="center"
                                        ),
                                    ],
                                )
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Font("Step 3. ", style={"color": "#999"}),
                                                "Sensors"
                                            ],
                                            width={"size": 4, "offset": 2},
                                            style={"font-weight": "600"},
                                            align="center"
                                        ),
                                        dbc.Col("# of sensors", style={"font-size": "15px"}, width={"size": 3, "offset": 1}, align="center"),
                                        dbc.Col(dbc.Input(value=2, type="number", min=2, max=3, step=1, id='sensor_number_input'), width=2),
                                    ],
                                )
                            ], 
                            width=6
                        ),
                    ]
                ),
                dbc.Row(html.P("")),
            ],
        ),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col("Type", width={'size': 3, 'offset': 1}, align="center"),
                                        dbc.Col(
                                            dcc.Dropdown(options=["Time Interval", "Realtime"], value="Time Interval", id="time_type"),
                                            width=5
                                        )
                                    ],
                                ),
                                #dbc.Row(
                                #    [
                                #        dbc.Col(html.P("Interval"), width={'size': 3, 'offset': 1}),
                                #        dbc.Col(
                                #            dcc.Dropdown(options=["second", "minute", "hour", "day", "week"], value="hour", ),
                                #            width=4
                                #        )
                                #    ]
                                #),
                                dbc.Row(
                                    [
                                        dbc.Col("Start", width={'size': 3, 'offset': 1}, align="center"),
                                        #dbc.Col(
                                        #    dbc.Input(type="text", id="start_time", className="form-control", style={"font-size": "18px", "font-family": " 'Work Sans', sans-serif", "font-weight": "400", "color": "#444"}),
                                        #    width=6
                                        #),
                                        dbc.Col(
                                            dcc.Input(type="datetime-local", id="start_time", step="1", style={"font-size": "18px", "font-family": " 'Work Sans', sans-serif", "font-weight": "400", "color": "#444", "text-align": "center"}),
                                            width=5
                                        )
                                    ],
                                    id="start_time_row"
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col("End", width={'size': 3, 'offset': 1}, align="center"),
                                        #dbc.Col(
                                        #    dbc.Input(type="text", id="end_time", className="form-control", style={"font-size": "18px", "font-family": " 'Work Sans', sans-serif", "font-weight": "400", "color": "#444"}),
                                        #    width=6
                                        #),
                                        dbc.Col(
                                            dcc.Input(type="datetime-local", id="end_time", step="1", style={"font-size": "18px", "font-family": " 'Work Sans', sans-serif", "font-weight": "400", "color": "#444", "text-align": "center"}),
                                            width=5
                                        ),
                                    ],
                                    id="end_time_row"
                                ),
                                #dbc.Row(dbc.Col(html.P(id="time_error", style={"color": "red"}), width={'size': 9, 'offset': 3})),
                            ],
                            width=6,
                            id="time_select"
                        ),
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col("Item", width={'size': 3, 'offset': 3}, align="center"),
                                        dbc.Col("Name", width={'size': 3, 'offset': 2}, align="center"),
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
        dbc.Container(
            dbc.Row(
                html.P(id="modal_error", style={"color": "red", "text-align": "center"}),
            )
        ),
        dbc.Container([dbc.Row(html.P("")), dbc.Row(dbc.Col(dbc.Button("OK", id="open_graph", color="primary", size="md", style={"font-size": "24px", "font-weight": "600"}, class_name="btn-block"), width=1), justify="center")]),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Chart",id="modal_chart_name", class_name="text-center w-100")),
                dbc.ModalBody(
                    [
                        dbc.Row(id="modal_graph"),
                        dbc.Row(
                            [
                                dbc.Col(id="modal_select_chart_type"),
                                dbc.Col(id="modal_select_sensor"),
                            ]
                        ),
                    ]
                ),
            ],
            id="modal",
            size="xl",
            is_open=False,
            style={"font-size": "18px", "font-family": " 'Work Sans', sans-serif", "font-weight": "400", "color": "#444"}
        ),
    ],
    style={"font-size": "18px", "font-family": " 'Work Sans', sans-serif", "font-weight": "400", "color": "#444"}, # sans-serif拿掉好像沒影響，但google font上面說要加我就加了
    class_name="dbc"
)

# callback要注意input和state的值是None的情況

@app.callback(
    Output('all_sensor_select', 'children'),
    Input('sensor_number_input', 'value'),
    Input('field_sensor', 'data'),
    State('all_sensor_select', 'children'),
)
def add_all_sensor_select_item(sensor_num, sensor_in_this_field, all_sensor_select):
    sensor_in_this_field = json.loads(sensor_in_this_field)

    if(len(sensor_in_this_field) < 2):
        sensor_num = len(sensor_in_this_field)

    ori_sensor_num = len(all_sensor_select) - 1
    if not sensor_num: # 如果sensor_num是None
        return dash.no_update

    if sensor_num > ori_sensor_num:
        for i in range(sensor_num - ori_sensor_num):
            all_sensor_select.append(
                dbc.Row(
                    [
                        dbc.Col(width={'size': 4, 'offset': 3}, id={"type": "sensor_item", "index": i + ori_sensor_num}, align="center"),
                        dbc.Col(
                            dcc.Dropdown(options=sensor_in_this_field, value=sensor_in_this_field[i + ori_sensor_num], id={"type": "sensor_select", "index": i + ori_sensor_num}),
                            width=5
                        ),
                    ],
                )
            )

    elif sensor_num < ori_sensor_num:
        all_sensor_select = all_sensor_select[0:sensor_num + 1] # 有1個row不是sensor select

    return all_sensor_select

@app.callback(
    Output('sensor_number_input', 'min'),
    Output('sensor_number_input', 'max'),
    Output('sensor_number_input', 'value'),
    Output('sensor_number_input', 'disabled'),
    Input('select_target', 'value'),
    Input('field_sensor', 'data'),
    State('sensor_number_input', 'value'),
)
def set_sensor_number_input_min_max(target, sensor_in_this_field, sensor_num):
    sensor_in_this_field = json.loads(sensor_in_this_field)

    if not target: # 若target是None，要disable sensor num的input
        return dash.no_update, dash.no_update, dash.no_update, True

    elif target == "Assess a relationship":
        if not sensor_num: # 若sensor_num是None, 仍要記得調整min和max, 且把value設為2
            return 2, 3, 2, False
        elif sensor_num < 2:
            return 2, 3, 2, False
        elif sensor_num > 3:
            return 2, 3, 3, False
        else:
            return 2, 3, sensor_num, False

    elif target == "Evaluate a distribution":
        if not sensor_num: # 若sensor_num是None, 仍要記得調整min和max, 且把value設為2
            return 1, 3, 2, False
        elif sensor_num > 3:
            return 1, 3, 3, False
        else:
            return 1, 3, sensor_num, False
    
    elif target == "Compare data":
        if not sensor_num: # 若sensor_num是None, 仍要記得調整min和max, 且把value設為2
            return 1, min(20, len(sensor_in_this_field)), 2, False
        else:
            return 1, min(20, len(sensor_in_this_field)), sensor_num, False

@app.callback(
    Output('Recommended_Chart', 'children'),
    Input('select_target', 'value'),
    Input('sensor_number_input', 'value'),
    State('sensor_number_input', 'min'),
    State('sensor_number_input', 'max'),
)
def decide_chart_type(target, sensor_num, sensor_num_min, sensor_num_max):
    ans = [html.Font("Recommended Chart Type: ", style={"color": "#999"})]

    if not target or not sensor_num or sensor_num < sensor_num_min or sensor_num > sensor_num_max: # 若target或sensor_num是None, 或sensor_num out of range
        ans.append("None")

    elif target == "Assess a relationship":
        if sensor_num == 2:
            ans.append("Scatter Chart")
        elif sensor_num == 3:
            ans.append("Bubble Chart")

    elif target == "Evaluate a distribution":
        if sensor_num == 1:
            ans.append("Column Histogram")
        elif sensor_num == 2:
            ans.append("Scatter Chart")
        elif sensor_num == 3:
            ans.append("3D Scatter Chart")
    
    elif target == "Compare data":
        if sensor_num == 2:
            ans.append("Bar Chart")
        else:
            ans.append("Line Chart")

    return ans

@app.callback(
    Output({'type': 'sensor_select', 'index': ALL}, 'value'),
    Input({'type': 'sensor_select', 'index': ALL}, 'value'),
    Input('field_sensor', 'data'),
)
def prevent_duplicate_sensor(new_sensor_selects, sensor_in_this_field):
    sensor_in_this_field = json.loads(sensor_in_this_field)

    ctx = dash.callback_context
    if ctx.triggered: # 若trigger非空，也就是sensor select真的有被改到
        trigger_index = int(ctx.triggered[0]["prop_id"].split(".")[0].split(",")[0].split(":")[1]) # 切出自己(被改的那個)的index並轉int
        for i in range(len(new_sensor_selects)): # 找有沒有人和自己選的sensor重複，有就把別人選的換掉
            if i != trigger_index and new_sensor_selects[trigger_index] and new_sensor_selects[i] == new_sensor_selects[trigger_index]: # 不能是自己、自己非None、且要和自己重複
                # 隨便找一個目前沒被選的sensor把新增的值換掉
                for no_used_sensor in sensor_in_this_field:
                    if no_used_sensor not in new_sensor_selects:
                        new_sensor_selects[i] = no_used_sensor
                        break
                break

    else:
        # 避免新增row時自動添加的sensor和原本的重複
        for i in range(len(new_sensor_selects)):
            if new_sensor_selects[i]: # 自己不是None
                for j in range(i + 1, len(new_sensor_selects)): #!!! 理論上只會新增的最多只有一個和自己，但就先當作可能有很多個所以不break了
                    if new_sensor_selects[i] == new_sensor_selects[j]: # 若新增的和自己重複
                        # 隨便找一個目前沒被選的sensor把新增的值換掉
                        for no_used_sensor in sensor_in_this_field:
                            if no_used_sensor not in new_sensor_selects:
                                new_sensor_selects[j] = no_used_sensor
                                break

    return new_sensor_selects

@app.callback(
    Output({'type': 'sensor_item', 'index': ALL}, 'children'),
    Input('Recommended_Chart', 'children'),
    State({'type': 'sensor_item', 'index': ALL}, 'children'),
)
def change_item_name(recommended_chart, sensor_items):
    recommended_chart = recommended_chart[1]
    if recommended_chart != "None":
        for i in range(min(len(chart_to_item_map[recommended_chart]), len(sensor_items))): #!!! 有出過一個奇怪的error，感覺是因為sensor num更新太快，為了避免那個error才選擇用min
            sensor_items[i] = chart_to_item_map[recommended_chart][i]

    return sensor_items

"""
@app.callback(
    Output('time_error', 'children'),
    Input('start_time', 'value'),
    Input('end_time', 'value'),
    Input('time_type', 'value'),
    prevent_initial_call=True
)
def check_start_end_time(start_time, end_time, time_type):
    if(time_type == "Time Interval" and start_time and end_time):
        datetime_start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        datetime_end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
        if(datetime_start_time >= datetime_end_time):
            return "TIME ERROR: End must bigger than Start."

    return ""
"""

@app.callback(
    Output('start_time_row', 'children'),
    Output('end_time_row', 'children'),
    Output('start_time', 'type'),
    Output('end_time', 'type'),
    Input('time_type', 'value'),
    State('start_time_row', 'children'),
    State('end_time_row', 'children'),
)
def check_time_type(time_type, start_time_row, end_time_row):
    if(time_type == "Time Interval"):
        if(len(start_time_row) == 1):
            start_time_row = [dbc.Col("Start", width={'size': 3, 'offset': 1}, align="center")] + start_time_row
            end_time_row = [dbc.Col("End", width={'size': 3, 'offset': 1}, align="center")] + end_time_row
        return start_time_row, end_time_row, 'datetime-local', 'datetime-local'

    else:
        if(len(start_time_row) > 1):
            start_time_row = start_time_row[1:2]
            end_time_row = end_time_row[1:2]
        return start_time_row, end_time_row, 'hidden', 'hidden'


@app.callback(
    Output('modal_error', 'children'),
    Output('open_graph', 'disabled'),
    Input('select_target', 'value'),
    Input('time_type', 'value'),
    Input('start_time', 'value'),
    Input('end_time', 'value'),
    Input('sensor_number_input', 'value'),
    Input({'type': 'sensor_select', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def check_condition_setting(select_target, time_type, start_time, end_time, sensor_number_input, sensor_select):
    if(not select_target):
        return "TARGET ERROR: Please choose a target.", True

    if(not time_type):
        return "TIME TYPE ERROR: Please choose a type.", True

    if(time_type == "Time Interval"): # Time Interval才要啟動start_time, end_time
        if((not start_time) or (not end_time)):
            return "TIME ERROR: Please set time.", True
        datetime_start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        datetime_end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
        if(datetime_start_time >= datetime_end_time):
            return "TIME ERROR: End must bigger than Start.", True

    if(not sensor_number_input):
        return "# OF SENSORS ERROR: Number out of range.", True

    for sensor in sensor_select:
        if(not sensor):
            return "SENSOR ERROR: Please choose every sensors.", True

    return "", False

@app.callback(
    Output("modal", "is_open"),
    Input("open_graph", "n_clicks"),
    State('modal_error', 'children'),
)
def open_modal_graph(n_clicks, modal_error):
    if(n_clicks and (not modal_error or modal_error == "")): # 避免剛載入時造成問題, 所以要確認n_clicks
        return True
    return False

@app.callback(
    Output('field_sensor', 'data'),
    Output('field_name', 'data'),
    Input("url", "pathname"),
)
def get_sensor(pathname):
    db.connect()
    session = db.get_session()
    sensor_in_this_field = []
    #field = "demo"
    field = pathname.split("/")
    field = field[len(field) - 1]
    for field_attr in (session.query(db.models.field).all()):
        #field_attr = session.query(db.models.field).filter(db.models.field.name == field) 不知道為什麼不能這樣用，下面的id會有問題
        if field_attr.name == field:
            query_df = (session.query(db.models.field_sensor)
                                .select_from(db.models.field_sensor)
                                .join(db.models.sensor)
                                .filter(db.models.field_sensor.field == field_attr.id)
                                .all())
            for sensor in query_df:
                sensor_in_this_field.append(sensor.df_name)

            break
    session.close()
    
    return json.dumps(sensor_in_this_field), field

@app.callback(
    Output('modal_chart_name', 'children'),
    Input('modal', 'is_open'),
    Input({'type': 'modal_chart_button', 'index': ALL}, 'n_clicks'),
    State({'type': 'modal_chart_button', 'index': ALL}, 'children'),
    State('Recommended_Chart', 'children'),
    prevent_initial_call=True
)
def set_modal_chart_name(is_open, modal_chart_button_click, modal_chart_button, Recommended_Chart):
    ctx = dash.callback_context
    if(not is_open):
        return dash.no_update

    elif(ctx.triggered[0]["prop_id"].split(".")[0] == "modal"): # 如果是按ok觸發的話, 設定成Recommended chart
        return Recommended_Chart[1]

    elif(not ctx.triggered[0]["value"]): # 第一次按OK時會有怪怪的情況 !!!不確定是否解決
        return dash.no_update

    else:
        trigger_index = int(ctx.triggered[0]["prop_id"].split(".")[0].split(",")[0].split(":")[1]) 
        return modal_chart_button[trigger_index]

@app.callback(
    Output('modal_select_chart_type', 'children'),
    Input('modal', 'is_open'),
    Input('modal_chart_name', 'children'),
    State('sensor_number_input', 'value'),
)
def set_modal_chart_button(is_open, modal_chart_name, sensor_number_input):
    if(not is_open):
        return dash.no_update

    ans = []
    for i in range(len(sensor_num_to_chart_map[sensor_number_input])):
        if(sensor_num_to_chart_map[sensor_number_input][i] == modal_chart_name): # 當前的chart type的按鈕要disable
            ans.append(dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            sensor_num_to_chart_map[sensor_number_input][i], 
                            id={"type": "modal_chart_button", "index": i}, 
                            disabled=True,
                            class_name="btn-block",
                            size="md",
                            style={"font-weight": "600"}
                        ),
                        width=5,
                        align="center"
                    ),
                    justify="center"
                )
            )
            ans.append(dbc.Row(html.P("")))
        else:
            ans.append(dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            sensor_num_to_chart_map[sensor_number_input][i], 
                            id={"type": "modal_chart_button", "index": i},
                            class_name="btn-block",
                            size="md",
                            style={"font-weight": "600"}
                        ),
                        width=5,
                        align="center"
                    ),
                    justify="center"
                )
            )
            ans.append(dbc.Row(html.P("")))

    return ans

@app.callback(
    Output('modal_select_sensor', 'children'),
    Input('modal', 'is_open'),
    State({'type': 'sensor_item', 'index': ALL}, 'children'),
    State({'type': 'sensor_select', 'index': ALL}, 'value'),
)
def set_modal_select_sensor(is_open, sensor_item, sensor_select):
    if(not is_open):
        return dash.no_update

    ans = [dbc.Row(
            [
                dbc.Col("Item", width={'size': 3}, align="center"),
                dbc.Col("Name", width={'size': 3, 'offset': 2}, align="center"),
            ]
        )
    ]
    for i in range(len(sensor_select)):
        ans.append(
            dbc.Row(
                [
                    dbc.Col(sensor_item[i], width={'size': 4}, id={"type": "modal_sensor_item", "index": i}, align="center"),
                    dbc.Col(
                        dcc.Dropdown(options=sensor_select, value=sensor_select[i], id={"type": "modal_sensor_select", "index": i}),
                        width=5
                    ),
                ],
            )
        )

    return ans

@app.callback(
    Output({'type': 'modal_sensor_select', 'index': ALL}, 'value'),
    Input({'type': 'modal_sensor_select', 'index': ALL}, 'value'),
    State({'type': 'sensor_select', 'index': ALL}, 'value'),
)
def prevent_duplicate_modal_sensor(modal_sensor_select, sensor_select):
    ctx = dash.callback_context
    if ctx.triggered: # 若trigger非空，也就是sensor select真的有被改到
        trigger_index = int(ctx.triggered[0]["prop_id"].split(".")[0].split(",")[0].split(":")[1]) # 切出自己(被改的那個)的index並轉int
        for i in range(len(modal_sensor_select)): # 找有沒有人和自己選的sensor重複，有就把別人選的換掉
            if i != trigger_index and modal_sensor_select[trigger_index] and modal_sensor_select[i] == modal_sensor_select[trigger_index]: # 不能是自己、自己非None、且要和自己重複
                # 隨便找一個目前沒被選的sensor把新增的值換掉
                for no_used_sensor in sensor_select:
                    if no_used_sensor not in modal_sensor_select:
                        modal_sensor_select[i] = no_used_sensor
                        break
                break

    else:
        # 避免新增row時自動添加的sensor和原本的重複
        for i in range(len(modal_sensor_select)):
            if modal_sensor_select[i]: # 自己不是None
                for j in range(i + 1, len(modal_sensor_select)): #!!! 理論上只會新增的最多只有一個和自己，但就先當作可能有很多個所以不break了
                    if modal_sensor_select[i] == modal_sensor_select[j]: # 若新增的和自己重複
                        # 隨便找一個目前沒被選的sensor把新增的值換掉
                        for no_used_sensor in sensor_select:
                            if no_used_sensor not in modal_sensor_select:
                                modal_sensor_select[j] = no_used_sensor
                                break

    return modal_sensor_select

@app.callback(
    Output({'type': 'modal_sensor_item', 'index': ALL}, 'children'),
    Input('modal_chart_name', 'children'),
    State({'type': 'modal_sensor_item', 'index': ALL}, 'children'),
)
def change_modal_item_name(modal_chart_name, modal_sensor_item):
    if modal_chart_name != "None":
        for i in range(min(len(chart_to_item_map[modal_chart_name]), len(modal_sensor_item))): #!!! 有出過一個奇怪的error，感覺是因為sensor num更新太快，為了避免那個error才選擇用min
            modal_sensor_item[i] = chart_to_item_map[modal_chart_name][i]

    return modal_sensor_item

@app.callback(
    Output('plot_interval', 'disabled'),
    Output('realtime_start_time', 'data'),
    Input('modal', 'is_open'),
    State('time_type', 'value'),
)
def set_interval_and_start_time(is_open, time_type):
    if(is_open and time_type == "Realtime"):
        return False, datetime.datetime.now()
    return True, dash.no_update

@app.callback(
    Output('modal_graph', 'children'),
    Input('modal', 'is_open'),
    Input({'type': 'modal_sensor_select', 'index': ALL}, 'value'),
    Input('modal_chart_name', 'children'),
    Input('plot_interval', 'n_intervals'),
    State('realtime_start_time', 'data'),
    State('time_type', 'value'),
    State('field_name', 'data'),
    State('start_time', 'value'),
    State('end_time', 'value'),
    
)
def plot(is_open, modal_sensor_select, modal_chart_name, plot_interval, realtime_start_time, time_type, field_name, start_time, end_time):
    if(not is_open or len(modal_sensor_select) == 0):
        return dash.no_update

    # from Farmdashboard/app/api.py's api_query_field_data
    db.connect()
    session = db.get_session()

    if(time_type == "Realtime"):
        start = realtime_start_time.replace('T', ' ')
        end = datetime.datetime.now()

    else:
        start = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
    
    i = 0
    res = []
    for df_name in modal_sensor_select:
        tablename = df_name.replace('-O', '')
        table = getattr(db.models, tablename)

        query = (session.query(table)
                        .select_from(table)
                        .join(db.models.field)
                        .filter(db.models.field.name == field_name))
        query = query.filter(table.timestamp >= start, table.timestamp <= end)

        res.append({df_name: [(str(record.timestamp), record.value) for record in query]})
        res[i] = pd.DataFrame(res[i])
        res[i]['Time'] = res[i][df_name].map(lambda x:x[0])
        res[i][df_name] = res[i][df_name].map(lambda x:x[1])

        i += 1

    if modal_chart_name == "Scatter Chart":
        for res_i in res:
            if 'df' in locals():
                df = df.merge(res_i, on='Time', how='inner', left_index=True, right_index=True)
            else:
                df = res_i
        fig = px.scatter(df, x=modal_sensor_select[0], y=modal_sensor_select[1], hover_name="Time")
    
    elif modal_chart_name == "Bubble Chart":
        for res_i in res:
            if 'df' in locals():
                df = df.merge(res_i, on='Time', how='inner', left_index=True, right_index=True)
            else:
                df = res_i
        fig = px.scatter(df,  x=modal_sensor_select[0], y=modal_sensor_select[1], size=modal_sensor_select[2], hover_name="Time", size_max=30)
    
    elif modal_chart_name == "Column Histogram":
        for res_i in res:
            if 'df' in locals():
                df = df.merge(res_i, on='Time', how='inner', left_index=True, right_index=True)
            else:
                df = res_i
        fig = px.histogram(df, x=modal_sensor_select[0])
    
    elif modal_chart_name == "3D Scatter Chart":
        for res_i in res:
            if 'df' in locals():
                df = df.merge(res_i, on='Time', how='inner', left_index=True, right_index=True)
            else:
                df = res_i
        fig = px.scatter_3d(df, x=modal_sensor_select[0], y=modal_sensor_select[1], z=modal_sensor_select[2], hover_name="Time")
    
    elif modal_chart_name == "Bar Chart": 
        #x = df["Time"]
        fig = go.Figure()
        for i in range(len(modal_sensor_select)):
            fig.add_trace(go.Bar(
                    x=res[i]["Time"],
                    y=res[i][modal_sensor_select[i]],
                    name=modal_sensor_select[i],
                    marker_color=chart_to_item_map["Bar Chart"][i]
                )
            )

        # Here we modify the tickangle of the xaxis, resulting in rotated labels.
        fig.update_layout(barmode='group', xaxis_tickangle=-45)
    
    elif modal_chart_name == "Line Chart":
        #x = df["Time"]
        raw_symbols = SymbolValidator().values
        namestems = []
        namevariants = []
        symbols = []
        for i in range(0,len(raw_symbols),3):
            name = raw_symbols[i+2]
            symbols.append(raw_symbols[i])
            namestems.append(name.replace("-open", "").replace("-dot", ""))
            namevariants.append(name[len(namestems[-1]):])
        fig = go.Figure()
        for i in range(len(modal_sensor_select)):
            fig.add_trace(go.Scatter(
                    marker_symbol=symbols[i * 4 + 2],
                    marker_size=8,
                    x=res[i]["Time"], 
                    y=res[i][modal_sensor_select[i]].values, 
                    mode='lines+markers', 
                    name=modal_sensor_select[i]
                )
            )

    fig.update_layout(
        font_family="times new roman",
        plot_bgcolor='white',
    )

    fig.update_xaxes(gridcolor='grey', zerolinecolor='grey')
    fig.update_yaxes(gridcolor='grey', zerolinecolor='grey')
    

    return dcc.Graph(figure=fig, style={'font-size': '30px'})