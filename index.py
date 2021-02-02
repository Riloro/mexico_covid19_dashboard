import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app, server
from layouts import layout1, layout2
import callbacks

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(Output(component_id='page-content', component_property='children'),
              Input(component_id='url', component_property='pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
         return layout1
    elif pathname == '/apps/app2':
         return layout2
    else:
        return layout1

if __name__ == '__main__':
    app.run_server(debug= True)