import dash

external_stylesheets = [
    'https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta1/dist/css/bootstrap.min.css'
]
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets= external_stylesheets)
app.title = 'Monitoreo COVID-19'
server = app.server