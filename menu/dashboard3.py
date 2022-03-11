from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from menu.style import *
from app import app, server
import numpy as np
import pandas as pd
from dash import dash_table
import plotly.express as px
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)

###########DataFrames######################
ga1 = pd.read_excel('2020 grouped.xlsx', header = 0, converters = {'fips':str})

##Pivot table by utility name 
table19 = pd.read_excel('2020 pivot.xlsx')

## Bottom 10 Saifi 
az19 = table19.head(10)

## Top 10 SAIFI
az19 = table19.tail(10)

##############################Graphs#####################################
# distribution circuits 2020
fig = px.choropleth(ga1, geojson = counties, locations='fips', color='SAIFI',
                            hover_name = ga1['Utility Characteristics|Utility Name'].tolist(),
		    	    hover_data = {'SAIFI':':,.2f', 
                                          'SAIDI':':,.2f'}, 
                           color_continuous_scale="Portland",
		    	   range_color = (0, 6),
                            scope = 'usa'
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_traces(hoverlabel_font_size =8, hoverlabel_align='right', selector=dict(type='choropleth'))

#SAIDI per county 
fig1 = px.choropleth(ga1, geojson = counties, locations='fips', color= 'SAIDI',
                            hover_name = ga1['Utility Characteristics|Utility Name'].tolist(),
                             hover_data = {'SAIFI':':,.2f', 
                                          'SAIDI':':,.2f'},
                           color_continuous_scale="Portland",
		     	   range_color = (0, 1500),
                            scope = 'usa'
                          )
fig1.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig1.update_traces(hoverlabel_font_size =8, hoverlabel_align='right', selector=dict(type='choropleth'))

############Style############################
styles = {
    'pre': {
	'height':'200px',
	'width':'400px',
	'overflow':'scroll',
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

######### Graph detail information #################
fig.update_layout(clickmode='event+select')

###############Mark text###################
yt = "2020 IEEE report" 
marktext1 = '''
### In 2020 U.S. power customers experienced an average of 8 hours of interruptions
In 2020, customers experienced just over 8 hours of electric power interruptions in 2020.
\n This is the most since data collection on electricity reliability began in 2013.
\n When major events are excluded, the average duration of interruptions customers experienced annually from 2013 to 2020 was consistently around two hours.
'''
mark1sc = html.Label(['Source here : ', html.A('EIA report 2019', href='https://www.eia.gov/todayinenergy/detail.php?id=50316')])
ut = html.Div(dcc.Markdown(children = marktext1))

mark2 = html.Div(className='row', children=[
        html.Div([
            dcc.Markdown("""
                **Hover Data**
                Mouse over values in the graph.
            """),
            html.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Click Data**
                Click on points in the graph. 'hovertext' shows utilities servicing the clicked on FIPs code area/county. 'customdata' shows the SAIFI and SAIDI score for the FIPs code area/county respectively. 
            """),
            html.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        html.Div([
            dcc.Markdown("""
                **Selection Data**
                Choose the lasso or rectangle tool in the graph's menu bar and then select points in the graph. 'hovertext' shows utilities servicing the clicked on FIPs code area/county. 'customdata' shows the SAIFI and SAIDI score for the FIPs code area/county respectively. 
                Note that selection data accumulates (or un-accumulates) selected data if you hold down the shift button while clicking.
            """),
            html.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns')
    ])



######################Graph layout ###########################
graph1 = dcc.Graph(
    id = 'graph1t',
    figure = fig, style={'width':'40%', 'display': 'inline-block'}
)

graph2 = dcc.Graph(
    id = 'graph2t',
    figure = fig1, style={'width':'40%', 'display': 'inline-block'}
)
                                  
####################################################
s = html.H1(yt, 
            style = {'color':'white', 'fontSize':50, 'txtAlign':'center', 'background-color':'Black', 'font-family':'courier'})
####################################################

########## LAYOUT #####################


BOX_STYLE3 = KOTAK_UTAMA_STYLE
SIDEBAR_STYLE3 = SIDEBAR_STYLE

#content
kolom_kiri3 = html.Div([s])
kolom_tengah3 = html.Div([ut, mark1sc])
kolom_kanan3 = html.Div([graph1, graph2])
kolom_peta3 = html.Div(mark2)

mainbox3 = html.Div([
    kolom_kiri3,
    kolom_tengah3,
    kolom_kanan3,
    kolom_peta3],id='main box3',
      style=BOX_STYLE3
                      )

#sidebar
sidebar3 = html.Div(
    [html.Img(src=app.get_asset_url('logo.png'),style={
                        'height':'116px', 
                        'width':'138px',
                        'margin-top': '-9px',
                        'background-color' : 'rgba(0,0,0,0.03)'}),
        #html.Hr(),
        html.P([
            "EIA", html.Br(),"Report", html.Br(), "2020"], className="lead", 
            style={
                'textAlign': 'center',
                'background-color' : 'rgba(0,0,0,0.03)',
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
    style=SIDEBAR_STYLE3,
)
content3 = html.Div([
            html.H1(['Dashboard III'],
              style={
              'margin-left': '340px',
              'margin-top': '20px',
              'color': 'rgba(255,255,255,1)',
              'fontSize': '18',
              }),     


             mainbox3,
            
              ],style={
              'margin-left': '0px',
              'margin-top': '0px',}
              )


layout3 = html.Div([dcc.Location(id="url"), sidebar3, content3])

