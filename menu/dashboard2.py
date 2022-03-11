from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash import dash_table 
from menu.style import *
from app import app, server
import numpy as np
import pandas as pd
import plotly.express as px	
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
###########DataFrames######################
ga1 = pd.read_excel('2019 grouped.xlsx', header = 0, converters = {'fips':str})

##Pivot table by utility name 
table19 = pd.read_excel('2019 pivot.xlsx')

## Bottom 10 Saifi 
az19 = table19.head(10)

## Top 10 SAIFI
az19 = table19.tail(10)

median = table19.SAIDI.median()

##############################Graphs#####################################
# distribution circuits 2019
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
fig1.update_layout(clickmode='event+select')

###############Mark text###################
yt = "2019 IEEE report" 
marktext1 = '''
### In 2019 U.S. power customers experienced an average of 5 hours of interruptions
In 2019, an average of 3.2 hours of interruptios were recorded during major events (storms, vegetation patterns, and utility practices). An average of 1.5 hours of interruptions without major events, in total nearly 5 hours total. 
\n From the data, the median SAIDI was {:,.2f}, in minutes.  
'''.format(median) 
mark1sc = html.Label(['Source here : ', html.A('EIA report 2019', href='https://www.eia.gov/todayinenergy/detail.php?id=45796#:~:text=In%202019%2C%20U.S.%20customers%20experienced,vegetation%20patterns%2C%20and%20utility%20practices.')])
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

BOX_STYLE2 = KOTAK_UTAMA_STYLE
SIDEBAR_STYLE2 = SIDEBAR_STYLE

#content
kolom_kiri2 = html.Div([s])
kolom_tengah2 = html.Div(children = [ut, mark1sc])
kolom_kanan2 = html.Div(children = [graph1, graph2])
kolom_peta2 = html.Div(children = [mark2])

mainbox2 = html.Div([
    kolom_kiri2,
    kolom_tengah2,
    kolom_kanan2,
    html.Br(),
    kolom_peta2],id='main box2',
   	style=BOX_STYLE2
                      )

#sidebar
sidebar2 = html.Div(
    [html.Img(src=app.get_asset_url('logo.png'),style={
                        'height':'116px', 
                        'width':'138px',
                        'margin-top': '-9px',
                        'background-color' : 'rgba(0,0,0,0.03)'}),
        #html.Hr(),
        html.P([
            "EIA", html.Br(),"Report", html.Br(), "2019"], className="lead", 
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
    style=SIDEBAR_STYLE2,
)
content2 = html.Div([
					  html.H1(['Dashboard II'],
					  	style={
					  	'margin-left': '340px',
					  	'margin-top': '20px',
					  	'color': 'rgba(255,255,255,1)',
					  	'fontSize': '18',
					  	}),			


					   mainbox2,
					  
					  	],style={
					  	'margin-left': '0px',
					  	'margin-top': '0px',}
					  	)

layout2 = html.Div([dcc.Location(id="url"), sidebar2, content2])

@app.callback(
    Output('hover-data', 'children'),
    Input('graph1t', 'hoverData'))
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    Input('graph1t', 'clickData'))
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    Input('graph1t', 'selectedData'))
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)





