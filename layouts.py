import dash_core_components as dcc
import dash_html_components as html


layout1 = html.Div([
    html.H3('App 1'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),

    #Bootstrap Card ..................
    html.Div([
        html.Div("Header", className = "card-header"),
        html.Div([
            html.H5("Card title", className = "card-title"),
            html.P( "Some quick example text to build on the card title and make up the bulk of the card's content.",
            className = "card-text"),
            html.A("Go somewhere", className = "btn btn-primary", href = "#")
        ],className = "card-body")


    ],className = "card border-danger mb-3", style={"width" : 288}),

    dcc.Link('Go to App 2', href='/apps/app2')
])

layout2 = html.Div([
    html.H3('App 2'),
    dcc.Dropdown(
        id='app-2-dropdown',
        options=[
            {'label': 'App 2 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-2-display-value'),
    dcc.Link('Go to App 1', href='/apps/app1')
])