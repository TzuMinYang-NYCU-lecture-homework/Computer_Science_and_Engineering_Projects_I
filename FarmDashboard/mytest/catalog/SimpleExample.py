from operator import truediv
import dash
#import dash_core_components as dcc
#import dash_html_components as html
from django_plotly_dash import DjangoDash
import dash_bootstrap_components as dbc
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State, MATCH, ALL
import datetime
from furl import furl

import sys
sys.path.append("..")
from db import db

db.connect()
session = db.get_session()
sensor_in_this_field = []
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
            sensor_in_this_field.append(sensor.df_name)

        break

session.close()

for i in sensor_in_this_field:
    print(i)

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
    "Line Chart": ["Red", "Orange", "Yellow", "Green", "Blue", "Black", "Purple"] #!!! 要20個 
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
        dcc.Store(id='field_sensor'),
        dcc.Location(id='url', refresh=False),
        html.P(id="test"),
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
        dbc.Container([dbc.Row(html.P("")), dbc.Row(dbc.Col(dbc.Button("OK", id="open_graph", color="primary", size="md", style={"font-size": "30px"}), width=1), justify="center")]),

        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("Header")),
                dbc.ModalBody("An extra large modal."),
            ],
            id="graph",
            size="xl",
            is_open=False,
        ),
    ],
    style={"font-size": "18px", "font-family": " 'Work Sans', sans-serif", "font-weight": "400", "color": "#444"}, # sans-serif拿掉好像沒影響，但google font上面說要加我就加了
    class_name="dbc"
)

# callback要注意input和state的值是None的情況

@app.callback(
    Output('all_sensor_select', 'children'),
    Input('sensor_number_input', 'value'),
    State('all_sensor_select', 'children'),
)
def add_all_sensor_select_item(sensor_num, all_sensor_select):
    ori_sensor_num = len(all_sensor_select) - 1
    if not sensor_num: # 如果sensor_num是None
        return dash.no_update

    if sensor_num > ori_sensor_num:
        for i in range(sensor_num - ori_sensor_num):
            all_sensor_select.append(
                dbc.Row(
                    [
                        dbc.Col(width={'size': 3, 'offset': 3}, id={"type": "sensor_item", "index": i + ori_sensor_num}, align="center"),
                        dbc.Col(
                            dcc.Dropdown(options=sensor_in_this_field, value=sensor_in_this_field[i + ori_sensor_num], id={"type": "sensor_select", "index": i + ori_sensor_num}),
                            width=6
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
    State('sensor_number_input', 'value')
)
def set_sensor_number_input(target, sensor_num):
    if not target: # 若target是None，要disable sensor num的input
        return dash.no_update, dash.no_update, dash.no_update, True

    elif not sensor_num: # 若sensor_num是None，什麼都不用動
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update

    elif target == "Assess a relationship":
        if sensor_num < 2:
            return 2, 3, 2, False
        elif sensor_num > 3:
            return 2, 3, 3, False
        else:
            return 2, 3, sensor_num, False

    elif target == "Evaluate a distribution":
        if sensor_num > 3:
            return 1, 3, 3, False
        else:
            return 1, 3, sensor_num, False
    
    elif target == "Compare data":
        return 1, min(20, len(sensor_in_this_field)), sensor_num, False

@app.callback(
    Output('Recommended_Chart', 'children'),
    Input('select_target', 'value'),
    Input('sensor_number_input', 'value'),
)
def decide_chart_type(target, sensor_num):
    ans = [html.Font("Recommended Chart Type: ", style={"color": "#999"})]

    if not target or not sensor_num: # 若target或sensor_num是None   
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
    Input({'type': 'sensor_select', 'index': ALL}, 'value')
)
def prevent_duplicate_sensor(new_sensor_selects):
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

@app.callback(
    Output('time_error', 'children'),
    Input('start_time', 'value'),
    Input('end_time', 'value'),
    prevent_initial_call=True
)
def check_start_end_time(start_time, end_time):
    if(start_time and end_time):
        datetime_start_time = datetime.datetime.strptime(start_time, '%Y-%m-%dT%H:%M:%S')
        datetime_end_time = datetime.datetime.strptime(end_time, '%Y-%m-%dT%H:%M:%S')
        if(datetime_start_time >= datetime_end_time):
            return "TIME ERROR: End must bigger than Start."

    return ""


@app.callback(
    Output('time_select', 'children'),
    Input('time_type', 'value'),
    State('time_select', 'children')
)
def check_time_type(time_type, time_select):
    if(time_type == "Time Interval"):
        time_select += [
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
                                    ),
                                ]
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
                                        width=4
                                    ),
                                ]
                            ),
                            dbc.Row(dbc.Col(html.P(id="time_error", style={"color": "red"}), width={'size': 9, 'offset': 3})),
                        ]
    else:
        time_select = time_select[0: 1]
    
    return time_select


@app.callback(
    Output('modal_error', 'children'),
    Output("graph", "is_open"),
    Input("open_graph", "n_clicks"),
    State("graph", "is_open"),
    State('time_error', 'children'),
    State('start_time', 'value'),
    State('end_time', 'value'),
    prevent_initial_call=True
)
def check_and_open_graph(n_clicks, is_open, time_error, start_time, end_time):
    error_msg = ""
    if((not start_time) or (not end_time)):
        error_msg = "TIME ERROR: Please set time."

    elif(n_clicks and time_error != ""):
        if(time_error == ""):
            is_open = True
        else:
            error_msg = "TIME ERROR: End must bigger than Start."

    return error_msg, is_open
    