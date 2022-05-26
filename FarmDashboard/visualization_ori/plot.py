# pip install plotly==5.6.0
# pip install pandas

import plotly.express as px
import plotly.graph_objects as go # for 3d
import numpy as np # for 3d
import pandas as pd
import plotly.figure_factory as ff # for line histogram

def scatter_plot(df):
    """
    #df = px.data.iris() # iris is a pandas DataFrame
    data = {
        "Time": ["2022-02-16 08:56:34.016038", "2022-02-16 08:56:36.016038", "2022-02-16 08:56:38.016038", "2022-02-16 08:56:40.016038", "2022-02-16 08:56:42.016038", "2022-02-16 08:56:44.016038", "2022-02-16 08:56:46.016038", "2022-02-16 08:56:48.016038"],
        "Bug1": [6.8, 5.1, 6.4, 3.2, 3.4, 5.3, 4.0, 3.5],
        "Temperature": [6.3, 5.0, 4.5, 5.1, 6.8, 4.3, 4.6, 3.2]
    }
    
    df = pd.DataFrame(data)
    #df.index = ["s1", "s2", "s3", "s4"]  #自訂索引值
    #df.columns = ["student_name", "math_score", "chinese_score"]  #自訂欄位名稱
    print(df)
    """
    #print(df.tail())
    fig = px.scatter(df, x="Temperature", y="Humidity", hover_name="Time")
    fig.show()

def bubble_plot(df):
    """
    data = {
        "Time": ["2022-02-16 08:56:34.016038", "2022-02-16 08:56:36.016038", "2022-02-16 08:56:38.016038", "2022-02-16 08:56:40.016038", "2022-02-16 08:56:42.016038", "2022-02-16 08:56:44.016038", "2022-02-16 08:56:46.016038", "2022-02-16 08:56:48.016038"],
        "Bug1": [6.8, 5.1, 6.4, 3.2, 3.4, 5.3, 4.0, 3.5],
        "Temperature": [6.3, 5.0, 4.5, 5.1, 6.8, 4.3, 4.6, 3.2],
        "AtPressure": [1.9, 3.9, 4.6, 4.4, 3.3, 6.4, 5.0, 1.0]
    }
    
    df = pd.DataFrame(data)
    print(df)
    """
    df =df[0:24 * 31]
    fig = px.scatter(df,  x="Temperature", y="Humidity", size="Bug1", hover_name="Time", size_max=30)
    fig.show()

def col_histogram_plot(df):
    """
    data = {
        "Time": ["2022-02-16 08:56:34.016038", "2022-02-16 08:56:36.016038", "2022-02-16 08:56:38.016038", "2022-02-16 08:56:40.016038", "2022-02-16 08:56:42.016038", "2022-02-16 08:56:44.016038", "2022-02-16 08:56:46.016038", "2022-02-16 08:56:48.016038"],
        "Bug1": [6.8, 5.1, 6.4, 5.3, 4.4, 5.3, 5.3, 3.5],
    }
    
    df = pd.DataFrame(data)
    print(df)

    """
    fig = px.histogram(df, x="Temperature")
    fig.show()

def threeD_surface_plot(df): # fail
    """
    data1 = {
        "Time": ["2022-02-16 08:56:34.016038", "2022-02-16 08:56:36.016038", "2022-02-16 08:56:38.016038", "2022-02-16 08:56:40.016038", "2022-02-16 08:56:42.016038", "2022-02-16 08:56:44.016038", "2022-02-16 08:56:46.016038", "2022-02-16 08:56:48.016038"],
        "Bug1": [6.8, 5.1, 6.4, 3.2, 3.4, 5.3, 4.0, 3.5],
        "Temperature": [6.3, 5.0, 4.5, 5.1, 6.8, 4.3, 4.6, 3.2],
        "AtPressure": [1.9, 3.9, 4.6, 4.4, 3.3, 6.4, 5.0, 1.0]
    }

    df = pd.DataFrame(data1)
    print(df)

    """
    x = df["Temperature"].values
    y = df["Humidity"].values
    z = df["Bug1"].values
    print(x, y, z)
    print(z.shape)

    """
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.show()
    fig.update_layout(title='Mt Bruno Elevation', autosize=True,
                    width=500, height=500,
                    margin=dict(l=65, r=50, b=65, t=90))
    fig.show()
    """
    """
    # Read data from a csv
    z_data = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/api_docs/mt_bruno_elevation.csv')
    #print(z_data)
    z = z_data.values
    print(z.shape)
    #print(z)
    sh_0, sh_1 = z.shape
    x, y = np.linspace(0, 1, sh_0), np.linspace(0, 1, sh_1)
    fig = go.Figure(data=[go.Surface(z=z, x=x, y=y)])
    fig.update_layout(title='Mt Bruno Elevation', autosize=False,
                    width=500, height=500,
                    margin=dict(l=65, r=50, b=65, t=90))
    fig.show()
    """

def three_D_scatter_chart(df):
    df = df[0:480]
    fig = px.scatter_3d(df, x='Temperature', y='Humidity', z='Bug1',
                        hover_name="Time")
    fig.show()

def line_three_var_plot(df):
    """
    data = {
        "Time": ["2022-02-16 08:56:34.016038", "2022-02-16 08:56:36.016038", "2022-02-16 08:56:38.016038", "2022-02-16 08:56:40.016038", "2022-02-16 08:56:42.016038", "2022-02-16 08:56:44.016038", "2022-02-16 08:56:46.016038", "2022-02-16 08:56:48.016038"],
        "Bug1": [6.8, 5.1, 6.4, 3.2, 3.4, 5.3, 4.0, 3.5],
        "Temperature": [6.3, 5.0, 4.5, 5.1, 6.8, 4.3, 4.6, 3.2],
        "AtPressure": [1.9, 3.9, 4.6, 4.4, 3.3, 6.4, 5.0, 1.0]
    }

    df = pd.DataFrame(data)
    print(df)
    """
    
    df =df[0:240]

    x = df["Time"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=df["Temperature"].values,
                        mode='lines', name='Temperature'))
    fig.add_trace(go.Scatter(x=x, y=df["Humidity"].values,
                        mode='lines', name='Humidity'))
    fig.add_trace(go.Scatter(x=x, y=df["Bug1"].values,
                        mode='lines', name='Bug1'))

    fig.show()

def line_two_var_plot(df):
    """
    data = {
        "Time": ["2022-02-16 08:56:34.016038", "2022-02-16 08:56:36.016038", "2022-02-16 08:56:38.016038", "2022-02-16 08:56:40.016038", "2022-02-16 08:56:42.016038", "2022-02-16 08:56:44.016038", "2022-02-16 08:56:46.016038", "2022-02-16 08:56:48.016038"],
        "Bug1": [6.8, 5.1, 6.4, 3.2, 3.4, 5.3, 4.0, 3.5],
        "Temperature": [6.3, 5.0, 4.5, 5.1, 6.8, 4.3, 4.6, 3.2],
        "AtPressure": [1.9, 3.9, 4.6, 4.4, 3.3, 6.4, 5.0, 1.0]
    }

    df = pd.DataFrame(data)
    print(df)
    """
    
    df =df[0:240]

    x = df["Time"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=df["Temperature"].values,
                        mode='lines', name='Temperature'))
    fig.add_trace(go.Scatter(x=x, y=df["Humidity"].values,
                        mode='lines', name='Humidity'))

    fig.show()

def line_one_var_plot(df):
    """
    data = {
        "Time": ["2022-02-16 08:56:34.016038", "2022-02-16 08:56:36.016038", "2022-02-16 08:56:38.016038", "2022-02-16 08:56:40.016038", "2022-02-16 08:56:42.016038", "2022-02-16 08:56:44.016038", "2022-02-16 08:56:46.016038", "2022-02-16 08:56:48.016038"],
        "Bug1": [6.8, 5.1, 6.4, 3.2, 3.4, 5.3, 4.0, 3.5],
        "Temperature": [6.3, 5.0, 4.5, 5.1, 6.8, 4.3, 4.6, 3.2],
        "AtPressure": [1.9, 3.9, 4.6, 4.4, 3.3, 6.4, 5.0, 1.0]
    }

    df = pd.DataFrame(data)
    print(df)
    """
    
    df =df[0:240]

    x = df["Time"]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=df["Temperature"].values,
                        mode='lines', name='Temperature'))

    fig.show()

def bar_two_var_chart(df):

    df =df[0:240]

    x = df["Time"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=df["Temperature"],
        name='Temperature',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=x,
        y=df["Humidity"],
        name='Humidity',
        marker_color='lightsalmon'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.show()

def bar_one_var_chart(df):

    df =df[0:24]

    x = df["Time"]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=x,
        y=df["Temperature"],
        name='Temperature',
        marker_color='indianred'
    ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(barmode='group', xaxis_tickangle=-45)
    fig.show()

def line_histogram(df):
    x1 = np.random.randn(200) - 1

    hist_data = df["Temperature"].values
    hist_data = [hist_data[0:200]]
    print(x1)
    print(hist_data)
    print(type(x1), type(hist_data), x1.shape, hist_data.shape)

    group_labels = ['Temperature']
    colors = ['#333F44']

    # Create distplot with curve_type set to 'normal'
    fig = ff.create_distplot(hist_data, group_labels, show_hist=False, colors=colors)

    # Add title
    fig.update_layout(title_text='Curve and Rug Plot')
    fig.show()

if __name__ == "__main__":
    df = pd.read_csv("data/data.csv")
    scatter_plot(df)
    #bubble_plot(df)
    #col_histogram_plot(df)
    ##threeD_surface_plot(df)
    #three_D_scatter_chart(df)
    #line_three_var_plot(df)
    #line_two_var_plot(df)
    #line_one_var_plot(df)
    
    #bar_two_var_chart(df)
    #bar_one_var_chart(df)
    #line_histogram(df)



"""
import dash
from dash import html
from dash import dcc
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
df = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig = px.scatter(df, x="gdp per capita", y="life expectancy",
                 size="population", color="continent", hover_name="country",
                 log_x=True, size_max=60)

app.layout = html.Div([
    dcc.Graph(
        id='life-exp-vs-gdp',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=False)
"""