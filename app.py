import dash 
app = dash.Dash(__name__, suppress_callback_exceptions = True)  #, assets_external_path = 'assets/') 
server = app.server 

app.scripts.config.serve_locally = True
