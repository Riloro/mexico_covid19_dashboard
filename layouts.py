import dash_core_components as dcc
import dash_html_components as html
import os

image_directory = os.getcwd() + "\images"

logo_url = "https://firebasestorage.googleapis.com/v0/b/imhere-e8e31.appspot.com/o/images%2Fvirus.png?alt=media&token=181e8b57-30b3-424f-a1ef-3890143e709c"

layout1 = html.Div([
    html.Header(
        html.Nav(html.A([
            html.Img(src=logo_url,
                     width="35",
                     height="35",
                     className="d-inline-block align-top",
                     alt=""), "Monitoreo COVID-19 "
        ],
                        className="navbar-brand"),
                 className="navbar navbar-dark bg-dark",
                 style=dict(backgroundColor="#cfd8dc"))),
    #Building a Bootstrap grid system .....
    html.Div(
        [  #Container
            html.Div(
                [  #Row1
                    html.Div(
                        [  #Column1
                            "Column 1"
                        ],
                        className="col-2"),
                    html.Div(
                        [  #Column2
                            html.Div(html.H1("Visualizando la pandemia por COVID-19"),
                                     className="d-flex  justify-content-center"),
                            html.Div(html.H1("en México"), className = "d-flex  justify-content-center"),
                            html.Div(className="w-100"),
                            html.Div([
                                html.H6("Última fecha de actualización : 31/12/2020")
                            ],className= "col-12  d-flex  justify-content-center")
                        ],
                        className="col-8"),
                    html.Div(
                        [  #Column3
                            "Column 3"
                        ],
                        className="col-2")
                ],
                className="row"),
            html.Div(
                [  #Row2
                    html.Div(
                        [  #Column1
                            "Column 1"
                        ],
                        className="col-2"),
                    html.Div(
                        [  #Column2
                            "Column 2"
                        ],
                        className="col-8"),
                    html.Div(
                        [  #Column3
                            "Column 3"
                        ],
                        className="col-2")
                ],
                className="row"),
        ],
        className="container"),
    dcc.Dropdown(id='app-1-dropdown',
                 options=[{
                     'label': 'App 1 - {}'.format(i),
                     'value': i
                 } for i in ['NYC', 'MTL', 'LA']]),
    html.Div(id='app-1-display-value'),

    #Bootstrap Card ..................
    html.Div([
        html.Div("Header", className="card-header"),
        html.Div([
            html.H5("Card title", className="card-title"),
            html.
            P("Some quick example text to build on the card title and make up the bulk of the card's content.",
              className="card-text"),
            html.A("Go somewhere", className="btn btn-primary", href="#")
        ],
                 className="card-body")
    ],
             className="card border-danger mb-3",
             style={"width": 288}),
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