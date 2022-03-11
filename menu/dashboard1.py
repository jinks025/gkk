from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import dash_table
import dash
from menu.style import *
from app import app, server
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
    
########################Set up dataframes for ranks and stats#############################
rel19 = pd.read_excel('2019 general rel.xlsx')
rel20 = pd.read_excel('2020 general rel.xlsx')

rel19['IEEE Standard|SAIFI With MED'] = rel19['IEEE Standard|SAIFI With MED'].astype(float)
rel20['IEEE Standard|SAIFI With MED'] = rel20['IEEE Standard|SAIFI With MED'].astype(float)

##Pivot table by utility name 
table19 = pd.read_excel('2019 pivot.xlsx') 
table20 = pd.read_excel('2020 pivot.xlsx') 

## Bottom 10 Saifi 
az19 = table19.head(10)
az20 = table20.head(10)

## Top 10 SAIFI
az191 = table19.tail(10)
az201 = table20.tail(10)

####################Components#################################
marktext1 = '''
### Utility System Reliability Measurements 
SAIDI, SAIFI, and CAIDI are the "big three" measurements. Reliability data is analyized in terms of momentary vs sustained interruptions. 
#### Momentary Interruption
IEEE defines a momentary interruption as “the brief loss of power delivery to one or more customers caused by the opening and closing operation of an interrupting device.” 
\n In general, these interruptions are defined as less than five minutes in length.
#### Sustained Interruption
IEEE defines sustained interruptions as any disruption lasting more than five minutes (e.g. any interruption longer than momentary). 
\n Some utilities using an even more rigorous 1-minute standard. 
#### SAIDI
System Average Interruption Duration Index. It's calculated by multiplying the average duration of customer interruptions by their total number and then dividing by the total number of customers in the system.
\n SAIDI describes total duration of the average customer interruption
#### SAIFI
System Average Interruption Frequency Index. It's calculated by dividing the total number of customers interrupted by an outage by the total number of customers in the system.
\n SAIFI describes how ***often*** an average customer experiences an interruption. SAIFI is improved by reducing frequency of outaches through 
\n better ***preventative maintenance***. 
#### CAIDI
Customer Average Interruption Duration Index. It's calculated as total minutes of customer interruption divided by the total number of customers interrupted.
\n CAIDI is useful for measuring response to interruptions, but not the prevention of interruptions. 
''' 

markprior = dcc.Markdown(children = f"### Top 10 worst reported SAIDI (in minutes) in 2019")
markcurr = dcc.Markdown(children = f"### Top 10 worst reported SAIDI (in minutes) in 2020")
markprior1 = dcc.Markdown(children = f"### Top 10 best reported SAIDI (in minutes) in 2019")
markcurr1 = dcc.Markdown(children = f"### Top 10 best reported SAIDI (in minutes) in 2020")
##############Dash tables###########################
table19 = dash_table.DataTable(id = 'prior', columns = [{'name':i, 'id':i} for i in az19.columns], data = az19.to_dict('records'), 
                              style_cell={'padding': '5px'},
    style_header={
        'backgroundColor': '#D3D3D3',
        'fontWeight': 'bold'
    })
table20 = dash_table.DataTable(id = 'current', columns = [{'name':i, 'id':i} for i in az20.columns], data = az20.to_dict('records'), 
                              style_cell={'padding': '5px'},
    style_header={
        'backgroundColor': '#D3D3D3',
        'fontWeight': 'bold'
    })
table191 = dash_table.DataTable(id = 'prior', columns = [{'name':i, 'id':i} for i in az191.columns], data = az191.to_dict('records'),
                               style_cell={'padding': '5px'},
    style_header={
        'backgroundColor': '#D3D3D3',
        'fontWeight': 'bold'
    })
table201 = dash_table.DataTable(id = 'current', columns = [{'name':i, 'id':i} for i in az201.columns], data = az201.to_dict('records'),
                               style_cell={'padding': '5px'},
    style_header={
        'backgroundColor': '#D3D3D3',
        'fontWeight': 'bold'
    })

####################################################

BOX_STYLE1 = KOTAK_UTAMA_STYLE
SIDEBAR_STYLE1 = SIDEBAR_STYLE

# content
header = html.Div(children = [dcc.Markdown(children = [marktext1])])
par = html.Div(children = [markprior, table19], style={'width':'35%', 'display':'inline-block', 'text-align':'center', 'border': '10px solid'})
graphsphere = html.Div(children = [markcurr, table20], style={'width':'35%', 'display':'inline-block', 'text-align':'center', 'border': '10px solid'})
aary = html.Div(children = [par, graphsphere])

par1 = html.Div(children = [markprior1, table191], style={'width':'35%', 'display':'inline-block', 'text-align':'center', 'border': '10px solid'})
graphsphere1 = html.Div(children = [markcurr1, table201], style={'width':'35%', 'display':'inline-block', 'text-align':'center', 'border': '10px solid'})
aary1 = html.Div(children = [par1, graphsphere1])

kotak_utama1 = html.Div([
    aary, 
    html.Br(),
    aary1, 
    html.Br(), 
    header], id='main box1',
    style=BOX_STYLE1
)

# sidebar
sidebar1 = html.Div(
    [html.Img(src=app.get_asset_url('logo.png'), style={
        'height': '116px',
        'width': '138px',
        'margin-top': '-9px',
        'background-color': 'rgba(0,0,0,0.03)'}),
     # html.Hr(),
     html.P([
         "Dashboard", html.Br(), "System Reliability", html.Br(), "Years 2019 vs 2020"], className="lead",
         style={
             'textAlign': 'center',
             'background-color': 'rgba(0,0,0,0.03)',
             'color': '#f1a633',
             'fontSize': '8',
             'margin-top': '-3px'
         }),
     html.Hr(),
     html.Div(children=[
         html.A(html.Button('DASHBOARD I', className='tab-button'),
                href='/dashboard1'),
         html.Hr(),
         html.A(html.Button('DASHBOARD II', className='tab-button'),
                href='/dashboard2'),
         html.Hr(),
         html.A(html.Button('DASHBOARD III', className='tab-button'),
                href='/dashboard3'),
         html.Hr(),
         html.A(html.Button('DASHBOARD IV', className='tab-button'),
                href='/dashboard4'),
         html.Hr(),
     ],

     ),
     ],
    style=SIDEBAR_STYLE1,
)
content1 = html.Div([
    html.H1(['Year 2019 vs Year 2020'],
            style={
                'margin-left': '340px',
                'margin-top': '20px',
                'color': 'rgba(255,255,255,1)',
                'fontSize': '18',
                'background-color':'black'
            }),

    kotak_utama1,

], style={
    'margin-left': '0px',
    'margin-top': '0px', }
)

layout1 = html.Div([dcc.Location(id="url"), sidebar1, content1])
