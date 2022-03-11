from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas as pd

from app import app, server

from menu.dashboard1 import *
from menu.dashboard2 import *
from menu.dashboard3 import *
from menu.dashboard4 import *

app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True

start = server 

sdbar = html.Div([])
ctnt = html.Div([])

def isi_sidebar():
    sidebar = html.Div([
              sdbar
              ], id='main_sidebar')
    return sidebar

def isi_content():
    content = html.Div(
              [ctnt],
              id='page-content'
        
              )
    return content

app.layout = html.Div([dcc.Location(id="url"),isi_sidebar(), isi_content()])

@app.callback(
    [Output(f"dashboard{i}", "active") for i in range(1, 5)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/" or "/dashboard1":
        # Treat page 1 as the homepage / index
        return True, False
    return [pathname == f"/dashboard{i}" for i in range(1, 5)]

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/dashboard1':  #'/' or '/dashboard1': -- '/' won't let the callback update profiles. Initial page will be empty. 
        ctnt = content1
        return ctnt

    elif pathname == '/dashboard2':
        ctnt = content2
        return ctnt

    elif pathname == '/dashboard3':
        ctnt = content3
        return ctnt

    elif pathname == '/dashboard4':
        ctnt = content4
        return ctnt

    else:
        return dbc.Container(
        [
            html.H1("Click on the tabs for more options", className="Wrong Page"),
            html.Hr(),
            html.P(f"Currently on {pathname}"),
        ]
    )

@app.callback(Output('main_sidebar', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname in ['/', '/dashboard1']:
        
        sdbar = sidebar1
        return sdbar

    elif pathname in ['/dashboard2']:
        
        sdbar = sidebar2
        return sdbar

    elif pathname in ['/dashboard3']:
        
        sdbar = sidebar3
        return sdbar

    elif pathname in ['/dashboard4']:
        
        sdbar = sidebar4
        return sdbar
    else:

        return ''

if __name__ == '__main__':
    app.run_server(debug=True)
    #app.run_server()
