from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import os
import pandas as pd
import plotly.express as px
import plotly.io as pio
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from app import app

logo_url = "https://firebasestorage.googleapis.com/v0/b/imhere-e8e31.appspot.com/o/images%2Fvirus.png?alt=media&token=181e8b57-30b3-424f-a1ef-3890143e709c"


#Readin JHU data ................................................................................................................................................
#Casos confirmados reportados por JHU ....
jhu_confirmed_time_serie = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv", encoding = "utf-8")
jhu_confirmed_mexico = jhu_confirmed_time_serie[jhu_confirmed_time_serie["Country/Region"] == "Mexico"]
#Muertes reportadas por JHU ...
jhu_deaths_time_serie = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",encoding="utf-8")
jhu_deaths_mexico = jhu_deaths_time_serie[jhu_deaths_time_serie["Country/Region"] == "Mexico"]
#Recuperados reportados por JHU ...
jhu_recovered_time_serie = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",encoding="utf-8")
jhu_recovered_mexico = jhu_recovered_time_serie[jhu_recovered_time_serie["Country/Region"] == "Mexico"]

raw_confirmed_data = jhu_confirmed_mexico.reset_index(drop=True).transpose().reset_index()
raw_deats_data = jhu_deaths_mexico.reset_index(drop = True).transpose().reset_index()
raw_recovered_data = jhu_recovered_mexico.reset_index(drop = True).transpose().reset_index()

#Filtrando el numero de casos y fechas de cada dataFrame ...
jhu_conf_mex_df = raw_confirmed_data["index"].iloc[4:].to_frame("fecha_confirmados").reset_index(drop = True)
jhu_conf_mex_df["confirmados"] = raw_confirmed_data[0].iloc[4:].reset_index(drop = True)
jhu_conf_mex_df["fecha_confirmados_dateTime"] = pd.to_datetime(jhu_conf_mex_df["fecha_confirmados"], format = "%m/%d/%y")

jhu_deaths_mex_df = raw_deats_data["index"].iloc[4:].to_frame("fecha_muerte").reset_index(drop = True)
jhu_deaths_mex_df["muertes"] = raw_deats_data[0].iloc[4:].reset_index(drop = True)
jhu_deaths_mex_df["fecha_muerte_dateTime"] = pd.to_datetime(jhu_deaths_mex_df["fecha_muerte"], format = "%m/%d/%y")

jhu_recovered_mex_df = raw_recovered_data["index"].iloc[4:].to_frame("fecha_recuperado").reset_index(drop = True)
jhu_recovered_mex_df["recuperados"] = raw_recovered_data[0].iloc[4:].reset_index(drop = True)
jhu_recovered_mex_df["feha_recuperados_dateTime"] = pd.to_datetime(jhu_recovered_mex_df["fecha_recuperado"], format = "%m/%d/%y")

#Reading national Data ...........................................................................................................................................
#data = pd.read_csv("http://datosabiertos.salud.gob.mx/gobmx/salud/datos_abiertos/datos_abiertos_covid19.zip", compression = "zip", encoding = "latin1")
#print("ARCHIVOS DE SALUD CARGADOS :)")
# States diccionary ...
# dics = pd.read_excel("https://github.com/Riloro/mexico_covid19_dashboard/blob/master/diccionarios/201128%20Catalogos_.xlsx?raw=true", sheet_name = None)
# dic_estados = dics["Catálogo de ENTIDADES"]
# #States population
# poblaciones = pd.read_csv("http://www.conapo.gob.mx/work/models/CONAPO/Datos_Abiertos/Proyecciones2018/pob_mit_proyecciones.csv", encoding="latin1")
# poblacion_2020 = poblaciones[poblaciones["AÑO"] == 2020]
# print("DATOS DE CONAPO CARGADOS :)")

#Last file update ..............................................................
date_last_update = jhu_conf_mex_df["fecha_confirmados_dateTime"].iloc[-1]
# last_update = data["FECHA_ACTUALIZACION"].iloc[0]
# date_last_update = datetime.strptime(last_update, '%Y-%m-%d')

if date_last_update.day < 10:
    day = "0" + str(date_last_update.day)
else:
    day = str(date_last_update.day)

if date_last_update.month < 10:
    month = "0" + str(date_last_update.month)
else:
    month = str(date_last_update.month)

str_last_update = day + "/" + month + "/" + str(date_last_update.year)

# Default template for all figures ...
pio.templates.default = "plotly_white"
#Reading data by state ....
datos_por_estado = pd.read_csv("https://raw.githubusercontent.com/Riloro/mexico_covid19_dashboard/master/processed_data/poblaciones_casos_por_estado.csv",
                                 encoding="latin1")

#List of states
lista_estados = list(datos_por_estado["ENTIDAD"]) # Estados ordenados por clave de entidad federativa

# Rate of confirmed case by 100,000 people
datos_por_estado["TASA DE CASOS POR 100K"] = 100000 * datos_por_estado["Casos confirmados"]/datos_por_estado["POBLACION"]
datos_por_estado.sort_values("TASA DE CASOS POR 100K", ascending = False, inplace = True)
datos_por_estado.reset_index(drop = True, inplace = True)
# Bar plot of the rate of confirmed cases per 100k persons
fig_bar_cases_rate = px.bar(x = datos_por_estado["ENTIDAD"], y = datos_por_estado["TASA DE CASOS POR 100K"],
                            labels = dict(y = "Casos confirmados / 100k personas" , x = "") ,title = "Tasa de casos confirmados por cada 100,000 personas")

fig_bar_cases_rate.update_traces(marker = dict(color = "#ff616f"))

# Groping by state ENTIDAD_RES and FECHA_INGRESO
confirmados_por_estado_fecha = pd.read_csv("https://raw.githubusercontent.com/Riloro/mexico_covid19_dashboard/master/processed_data/confirmados_por_estado.csv",
                                            encoding="latin1")
confirmados_por_estado_fecha["fecha_ingreso"] = pd.to_datetime(confirmados_por_estado_fecha["FECHA_INGRESO"], format = "%Y-%m-%d")

defunciones_por_estado_fecha = pd.read_csv("https://raw.githubusercontent.com/Riloro/mexico_covid19_dashboard/master/processed_data/defunciones_por_estado.csv",
                                            encoding="latin1")
defunciones_por_estado_fecha["fecha_defuncion"] = pd.to_datetime(defunciones_por_estado_fecha["FECHA_DEF"], format = "%Y-%m-%d")

entidad_clave = datos_por_estado["ENTIDAD"].to_frame()
entidad_clave["CLAVE_ENTIDAD"] = datos_por_estado["CLAVE_ENTIDAD"]
# Merge between entidad_cave and confirmados_por_estado_fecha
confirmados_por_estado_fecha_clave = pd.merge(confirmados_por_estado_fecha, entidad_clave, how = "left", left_on = "ENTIDAD_RES", right_on = "CLAVE_ENTIDAD")
# Merge betweem entidad_clave and defunciones_por_estado_fecha
defunciones_por_estado_fecha_clave = pd.merge(defunciones_por_estado_fecha, entidad_clave, how = "left", left_on = "ENTIDAD_RES", right_on = "CLAVE_ENTIDAD")


#Insert a character in the ith position
def insert_str(init_str, insert_str, i):
    return init_str[:i] + insert_str + init_str[i:]
#Insert commas in a str .............................
def insert_commas(string):
    step = 3
    size = len(string)
    quotient = size//step
    mod = size % step

    if mod == 0:
        commas_number = quotient - 1
        init_index = step
    else:
        commas_number = quotient
        init_index = mod

    for i in range(commas_number):
        string = insert_str(string, ",", init_index )
        init_index = init_index + step + 1
    return string

# Computing the comulative cases ...
def commulative_cases(data):
    data_vec = np.array(data)
    data_acumulados = np.cumsum(data_vec)
    return pd.Series(data_acumulados)                # Numpy array to pandas Serie

# Ploting the commulative confirmed and deaths cases ...
def acum_plot(x_conf_data, y_conf_data, x_def_data, y_def_data, region ):
    fig_acum = go.Figure()

    fig_acum.add_trace(go.Scatter(x = x_conf_data, y = y_conf_data,
                    mode = "lines" , line = dict(color = "#ff1744", width = 2.5), name = "Casos confirmados" ))

    fig_acum.add_trace(go.Scatter(x = x_def_data, y = y_def_data,
                    mode = "lines", line = dict(color = "black", width = 2.5), name = "Defunciones "))

    fig_acum.update_xaxes(title = "Fecha de registro")
    fig_acum.update_yaxes(title = "Número de casos acumulados")
    fig_acum.update_layout(title = "Casos acumulados en " + region , hovermode = "x unified")
    return fig_acum

#Computing the average with the actual day plus the 6 previous days
def average_of_seven_days(serie , threshold = 25000):
    data_vect = np.array(serie)
    average = np.zeros(data_vect.size)
    counter = 0
    init = 0
    # ....
    index = np.nonzero(data_vect > threshold)
    data_vect[index] = 0
    #Computing the average
    for i in range(data_vect.size):
        if i >= 6:
            average[counter] = np.mean(data_vect[init:i+1])
            init += 1
        else:
            average[counter] = 1/7 * np.sum(data_vect[0:i+1])

        counter += 1

    return  pd.Series(np.round(average))   #Return a pandas Serie with rounded values

# Bar plots for confirmed and death cases ...
def show_confirmed_cases(x_vect,y_vect, region, anomalia):

    if anomalia == True:
        h = 600
        w = 1000
    else:
        h = 450
        w = 900

    fig_bar1 = go.Figure()
    fig_bar1.add_trace(go.Bar(x = x_vect, y = y_vect,
                                marker = dict(color = "#ff1744", opacity = 0.6 ), name = "Nuevos casos"))
    #Average of seven days curve ...
    fig_bar1.add_trace(go.Scatter(x = x_vect, y =  average_of_seven_days(y_vect),
                                        mode = "lines", line = dict(color = "#b71c1c", width = 2.5), name = "Promedio de 7 días"))
    #custom layout
    fig_bar1.update_xaxes(title = "Fecha de registro",spikethickness= .4)
    fig_bar1.update_yaxes(title = "Nuevos casos confirmados")
    fig_bar1.update_layout(width = w, height = h, hovermode = "x unified", title = "Nuevos casos de COVID-19 reportados diariamente en " + region)
    #Showing figure ...
    return fig_bar1

def show_deaths(x_vect,y_vect,region, anomalia):

    if anomalia == True:
        h = 600
        w = 1000
    else:
        h = 450
        w = 900
    # Death cases ...
    fig_bar2 = go.Figure()
    fig_bar2.add_trace(go.Bar(x = x_vect, y = y_vect,
                                marker = dict(color = "#546e7a", opacity = 0.75), name = "Nuevas defunciones"))
    #Average of seven days curve ...
    fig_bar2.add_trace(go.Scatter(x = x_vect, y =average_of_seven_days(y_vect, threshold = 2500),
                                        mode = "lines", line = dict(color = "black", width = 2.5), name = "Promedio de 7 días"))
    #custom layout
    fig_bar2.update_xaxes(title = "Fecha de registro",spikethickness= .4)
    fig_bar2.update_yaxes(title = "Nuevas defunciones confirmadas")
    fig_bar2.update_layout(width = w, height = h, hovermode = "x unified", title = "Nuevas defunciones de COVID-19 reportadas diariamente en " + region)
    #Showing figure ...
    return fig_bar2

# difference JHU data in order to get daily cases ....
def diff(data):
    v_1 = np.array(data)
    v_2 = np.diff(v_1)
    res = np.insert(v_2,0,v_1[0])

    return pd.Series(res)

#JHU data figures .....................................................................................................................
#Graficando los casos confirmados de muertes y confirmados ....
jhu_mex_acum_fig = acum_plot(jhu_conf_mex_df["fecha_confirmados_dateTime"], jhu_conf_mex_df["confirmados"],
            jhu_deaths_mex_df["fecha_muerte_dateTime"], jhu_deaths_mex_df["muertes"], region="México")

#Getting daily cases ...
jhu_conf_daily = diff(jhu_conf_mex_df["confirmados"])
jhu_conf_mex_df["casos diarios"] = jhu_conf_daily

#Getting daily deaths...
jhu_daily_deaths = diff(jhu_deaths_mex_df["muertes"])
jhu_deaths_mex_df["muertes diarias"] = jhu_daily_deaths

daily_cases_mex_fig = show_confirmed_cases(jhu_conf_mex_df["fecha_confirmados_dateTime"],jhu_conf_mex_df["casos diarios"], region = "México", anomalia = True)
daily_deaths_mex_fig = show_deaths(jhu_deaths_mex_df["fecha_muerte_dateTime"], jhu_deaths_mex_df["muertes diarias"],  region = "México", anomalia = True)

#Getting comulative cases separated by commas ....
str_conf_mex = str(jhu_conf_mex_df["confirmados"].iloc[-1])
str_deaths_mex = str(jhu_deaths_mex_df["muertes"].iloc[-1])
str_recovered_mex = str(jhu_recovered_mex_df["recuperados"].iloc[-1])
#Calling inset_commas function ...
str_conf_mex_commas = insert_commas(str_conf_mex)
str_recovered_mex_commas = insert_commas(str_recovered_mex)
str_deaths_mex_commas = insert_commas(str_deaths_mex)

layout1 = html.Div([
    html.Header(
        html.Nav(html.Div(html.A([
            html.Img(src=logo_url,
                     width="35",
                     height="35",
                     className="d-inline-block align-top",
                     alt=""), "Monitoreo COVID-19 "
        ],
                                 className="navbar-brand"),
                          className="container-fluid"),
                 className="navbar navbar-expand-sm navbar-dark bg-dark",
                 style=dict(backgroundColor="#cfd8dc"))),
    #Building a Bootstrap grid system .....
    html.Div(
        [  #Container
            html.Div(
                [  #Row1
                    html.Div(
                        [  #Column1
                        ],
                        className="col-2"),
                    html.Div(
                        [  #Column2
                            html.Div(html.H1(
                                ["Visualizando la pandemia por COVID-19"]),
                                     className="d-flex  justify-content-center"
                                     ),
                            html.Div(
                                html.H1("en México"),
                                className="d-flex  justify-content-center"),
                            html.Div(className="w-100"),
                            html.Div([
                                html.H6("Última fecha de actualización : " +
                                        str_last_update)
                            ],
                                     className=
                                     "col-12  d-flex  justify-content-center"),
                            html.Div(className="w-100")
                        ],
                        className="col-8 p-5"),
                    html.Div(
                        [  #Column3                        
                        ],
                        className="col-2")
                ],
                className="row"),
            html.Div(
                [  #Row2
                    html.Div(
                        [  #Column1
                            #Bootstrap Card ..................
                            html.Div([
                                html.Div(
                                    "Confirmados acumulados",
                                    className=
                                    "card-header d-flex justify-content-center"
                                ),
                                html.Div(
                                    [
                                        html.H5(str_conf_mex_commas,
                                                className="card-title"),
                                    ],
                                    className=
                                    "card-body d-flex justify-content-center")
                            ],
                                     className="card border-danger mb-3",
                                     style={"width": 270}),
                        ],
                        className="col d-flex justify-content-center"),
                    html.Div(
                        [  #Column2
                            html.Div([
                                html.Div(
                                    "Defunciones acumuladas",
                                    className=
                                    "card-header d-flex justify-content-center"
                                ),
                                html.Div(
                                    [
                                        html.H5(str_deaths_mex_commas,
                                                className="card-title"),
                                    ],
                                    className=
                                    "card-body d-flex justify-content-center")
                            ],
                                     className="card border-dark mb-3",
                                     style={"width": 270}),
                        ],
                        className="col d-flex justify-content-center"),
                    html.Div(
                        [  #Column3
                            html.Div([
                                html.Div(
                                    "Recuperados acumulados",
                                    className=
                                    "card-header d-flex  justify-content-center"
                                ),
                                html.Div(
                                    [
                                        html.H5(str_recovered_mex_commas,
                                                className="card-title"),
                                    ],
                                    className=
                                    "card-body d-flex  justify-content-center")
                            ],
                                     className="card border-success mb-3",
                                     style={"width": 270}),
                        ],
                        className="col d-flex justify-content-center")
                ],
                className="row"),
            html.Div(
                [  #Row3
                    html.Div(
                        [  #Column1
                        ],
                        className="col-2"),
                    html.Div(
                        [  #Column2
                            html.Div(className="w-100"),
                            html.Div(
                                [
                                    dcc.Graph(id="national_cases",
                                              figure=daily_cases_mex_fig)
                                ],
                                className="d-flex  justify-content-center"),
                            html.Div(className="w-100"),
                            html.Div(
                                [
                                    dcc.Graph(id="national_deaths",
                                              figure=daily_deaths_mex_fig)
                                ],
                                className="d-flex  justify-content-center"),
                            html.Div([
                                dcc.Markdown('''
                                _*El día **5 de octubre del 2020 los datos reportados presentan anomalías**. Dichas anomalías fueron excluidas del cálculo del promedio de 7 días._
                                ''')
                            ]),
                            html.Div(
                                [
                                    dcc.Graph(id="national_acum",
                                              figure=jhu_mex_acum_fig)
                                ],
                                className="d-flex  justify-content-center"),
                            html.Div(html.H4(
                                "Situación actual de la pandemia por entidad federativa"
                            ),
                                     className='p-3'),
                            html.Div(
                                dcc.Graph(id="rate_per_100k",
                                          figure=fig_bar_cases_rate),
                                className="d-flex  justify-content-center"),
                            html.Div(
                                dcc.Dropdown(id='state_selector',
                                             options=[{
                                                 'label': v,
                                                 'value': i
                                             } for i, v in enumerate(
                                                 lista_estados)],
                                             value=0)),
                            html.Div(html.P(id="p_test")),
                            html.Div(
                                dcc.Graph(id="conf_cases_edo"),
                                className="d-flex  justify-content-center"),
                            html.Div(
                                dcc.Graph(id="deaths_edo"),
                                className="d-flex  justify-content-center"),
                            html.Div(
                                dcc.Graph(id="cum_edo"),
                                className="d-flex  justify-content-center")
                        ],
                        className="col-8"),
                    html.Div(
                        [  #Column3
                        ],
                        className="col-2")
                ],
                className="row"),
        ],
        className="container")
])

layout2 = html.Div(["HOLI"])

#CallBack dropDown function ...
@app.callback(Output('conf_cases_edo', 'figure'),
              Output('deaths_edo','figure'),
              Output('cum_edo','figure'),
              [Input('state_selector', 'value')])
def update_state_fig(value):
    clave_estado = value + 1
    confirmados_estado = confirmados_por_estado_fecha_clave[confirmados_por_estado_fecha_clave["ENTIDAD_RES"] == clave_estado]
    print("Total de casos confirmados = ",confirmados_estado["confirmados"].sum())
    confirmados_estado.reset_index(drop = True, inplace = True)
    confirmados_estado["confirmados_acumulados"] = commulative_cases(confirmados_estado["confirmados"]) # Accumulated confirmed cases in Mich.
    defunciones_estado = defunciones_por_estado_fecha_clave[defunciones_por_estado_fecha_clave["ENTIDAD_RES"] == clave_estado ]
    print("Total de defunciones acumuladas = ", defunciones_estado["defunciones"].sum())
    defunciones_estado.reset_index(drop = True, inplace = True)
    defunciones_estado["defunciones_acumuladas"] = commulative_cases(defunciones_estado["defunciones"])

    #State commulative cases figure....
    acum_edo = acum_plot(confirmados_estado["fecha_ingreso"],confirmados_estado["confirmados_acumulados"],
                        defunciones_estado["fecha_defuncion"], defunciones_estado["defunciones_acumuladas"], region = confirmados_estado["ENTIDAD"].iloc[0] )

    conf_cases_edo = show_confirmed_cases(confirmados_estado["fecha_ingreso"],confirmados_estado["confirmados"], region = confirmados_estado["ENTIDAD"].iloc[0], anomalia = False)
    deaths_edo = show_deaths(defunciones_estado["fecha_defuncion"],defunciones_estado["defunciones"], region = confirmados_estado["ENTIDAD"].iloc[0], anomalia = False)

    return conf_cases_edo, deaths_edo, acum_edo