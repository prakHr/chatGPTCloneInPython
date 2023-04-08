import dash
from dash import Dash, dcc, callback, Output, State, Input, dash_table # pip install dash
import dash_bootstrap_components as dbc # pip install dash-bootstrap-components
from dash import html
import plotly.express as px
import pandas as pd
import os
from dash_bootstrap_templates import ThemeChangerAIO, template_from_url
app = Dash(__name__, use_pages=True,external_stylesheets=[dbc.themes.MORPH],pages_folder="pages")
   
    

graph = html.Div(
    html.Div([
        dcc.Store(id="stored-data",data={'email':'','password':''},storage_type = 'session'),
        dash.page_container
    ],
    id="theme-changer-div",
    className="m-4")
)
theme_change = ThemeChangerAIO(aio_id="theme")

app.layout = dbc.Container([theme_change,graph],className = "m-4 dbc")

@app.callback(
    Output("theme-changer-div","id"),
    Input(ThemeChangerAIO.ids.radio("theme"),"value"),
)
def update_graph_theme(theme):
    template=template_from_url(theme)
    return template



server = app.server
if __name__ == "__main__":

    app.run_server(debug=True)
