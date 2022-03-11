from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import dash
from dash import dash_table 
from menu.style import *
from app import app, server
import pandas as pd
import numpy as np 
#################DATAFRAMES##################
table20 = pd.read_excel('2020 pivot.xlsx')
table19 = pd.read_excel('2019 pivot.xlsx')

############ tables #################

table1 = dash_table.DataTable(
    id = 'datatable',
    columns = [{'name': i, 'id': i} for i in table19.columns],
    page_current = 0,
    page_size = 20,
    page_action = 'custom',
    filter_action= 'custom',
    filter_query= ''
)

table2 = dash_table.DataTable(
    id = 'datatable2',
    columns = [{'name': i, 'id': i} for i in table20.columns],
    page_current = 0,
    page_size = 20,
    page_action = 'custom',
    filter_action= 'custom',
    filter_query= ''
)

##################Mark Down#######################
mark1 = html.Div([dcc.Markdown(''' ***2019*** ''')])
mark2 = html.Div([dcc.Markdown(''' ***2020*** ''')])

##################################################

# Add dashboard specific methods here

BOX_STYLE4 = KOTAK_UTAMA_STYLE
SIDEBAR_STYLE4 = SIDEBAR_STYLE

#content
kolom_kiri4 = html.Div([mark1])
kolom_tengah4 = html.Div([table1],style={'width':'40%', 'display': 'inline-block'})
kolom_kanan4 = html.Div([mark2])
kolom_peta4 = html.Div([table2],style={'width':'40%', 'display': 'inline-block'})

mainbox4 = html.Div([
    kolom_kiri4,
    kolom_tengah4,
    kolom_kanan4,
    kolom_peta4],id='main box4',
      style=BOX_STYLE4
                      )

#sidebar
sidebar4 = html.Div(
    [html.Img(src=app.get_asset_url('logo.png'),style={
                        'height':'116px', 
                        'width':'138px',
                        'margin-top': '-9px',
                        'background-color' : 'rgba(0,0,0,0.03)'}),
        #html.Hr(),
        html.P([
            "Datasource", html.Br(),"for", html.Br(), "2019 vs 2020"], className="lead", 
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
    style=SIDEBAR_STYLE4,
)
content4 = html.Div([
            html.H1(['Dashboard IV'],
              style={
              'margin-left': '340px',
              'margin-top': '20px',
              'color': 'rgba(255,255,255,1)',
              'fontSize': '18',
              }),     


             mainbox4,
            
              ],style={
              'margin-left': '0px',
              'margin-top': '0px',}
              )


layout4 = html.Div([dcc.Location(id="url"), sidebar4, content4])

#####################CALL BACKS###################

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3

@app.callback(
    Output('datatable', "data"),
    Input('datatable', "page_current"),
    Input('datatable', "page_size"),
    Input('datatable', "filter_query"))
def update_table(page_current, page_size, filter):
    print(filter)
    filtering_expressions = filter.split(' && ')
    ga2 = pd.DataFrame(table19)
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
	
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            ga2 = ga2.loc[getattr(ga2[col_name], operator)(filter_value)]
        elif operator == 'contains':
            ga2 = ga2.loc[ga2[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            ga2 = ga2.loc[ga2[col_name].str.startswith(filter_value)]

    return ga2.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')

@app.callback(
    Output('datatable2', "data"),
    Input('datatable2', "page_current"),
    Input('datatable2', "page_size"),
    Input('datatable2', "filter_query"))
def update_table(page_current, page_size, filter):
    print(filter)
    filtering_expressions = filter.split(' && ')
    ga2 = pd.DataFrame(table20)
    for filter_part in filtering_expressions:
        col_name, operator, filter_value = split_filter_part(filter_part)
	
        if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
            # these operators match pandas series operator method names
            ga2 = ga2.loc[getattr(ga2[col_name], operator)(filter_value)]
        elif operator == 'contains':
            ga2 = ga2.loc[ga2[col_name].str.contains(filter_value)]
        elif operator == 'datestartswith':
            # this is a simplification of the front-end filtering logic,
            # only works with complete fields in standard format
            ga2 = ga2.loc[ga2[col_name].str.startswith(filter_value)]

    return ga2.iloc[
        page_current*page_size: (page_current + 1)*page_size
    ].to_dict('records')

