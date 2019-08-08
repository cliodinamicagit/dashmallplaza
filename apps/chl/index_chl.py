import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from components.functions import update_mapbox
import plotly.graph_objs as go
from app import app
import numpy as np
import pandas as pd

########################################################################################################################
# FUNTIONS
########################################################################################################################
columna = ['name', 'pais_iso3', 'id_comuna', 'id_region', 'classification']
df = pd.read_csv('data/chl/etl_geo_datos_all.csv', usecols=columna, delimiter=';', encoding='latin-1')
dfs = df[(df.pais_iso3 == 'CHL') & (df.classification == 'Mall')]


def update_sensacion(id_comuna):
    url = 'data/chl/etl_sensacion.csv'  # TODO: API Falta
    df = pd.read_csv(url, delimiter=';', encoding='latin-1')
    df_fil = df.query('id_comuna == "' + str(id_comuna) + '"')

    def figure_omil(df):
        trace1 = go.Scatter(
            x=df['ano'],
            y=df['Personas_capacitacion'],
            mode='markers+lines',
            name='Capacitacion',
            line=dict(
                color=('black'),
                width=2, ),
        )
        trace2 = go.Scatter(
            x=df['ano'],
            y=df['Personas_empleo'],
            mode='markers+lines',
            name='Empleo',
            line=dict(
                color=('darkred'),
                width=2, ),
        )
        data = [trace1, trace2]

        layout = go.Layout(

            xaxis={'tickmode': 'linear', 'tick0': '1'},
            # yaxis={'title': 'Cantidad'},
            dragmode=False,
            font={'size': 9},
            height=80,
            margin={'l': 30, 'b': 10, 't': 20, 'r': 10},
            # legend={'orientation': "h"},
            legend=dict(orientation='h', x=0, y=1.3, bgcolor='rgba(0,0,0,0)'),
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Busqueda de Capacitación y Empleo',

        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_fuerza(df):
        trace1 = go.Scatter(
            x=df['ano'],
            y=df['Fuerza_Trabajo'],
            mode='lines+markers',
            name='Fuerza_Trabajo',
            line=dict(
                color=('darkred'),
                width=2, ),
        )

        data = [trace1]

        layout = go.Layout(
            xaxis={'tickmode': 'linear', 'tick0': '1'},
            # yaxis={'title': 'Cantidad'},
            dragmode=False,
            font={'size': 9},
            height=70,
            margin={'l': 20, 'b': 10, 't': 20, 'r': 10},
            legend=dict(orientation='h', bgcolor='rgba(0,0,0,0)'),
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Fuerza de Trabajo'
        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_fonasa(df):
        trace1 = go.Bar(
            x=df['ano'],
            y=df['FONASA_A'],
            marker=dict(color=('darkred')),
            name='Tramo A',

        )
        trace2 = go.Bar(
            x=df['ano'],
            y=df['FONASA_B'],
            marker=dict(color=('#657b5b')),
            name='Tramo B',

        )
        trace3 = go.Bar(
            x=df['ano'],
            y=df['FONASA_C'],
            marker=dict(color=('#412f55')),
            name='Tramo C',

        )
        trace4 = go.Bar(
            x=df['ano'],
            y=df['FONASA_D'],
            marker=dict(color=('#7a7214')),
            name='Tramo D',

        )
        data = [trace1, trace2, trace3, trace4]

        layout = go.Layout(
            xaxis={'range': [2012, 2019]},
            # yaxis={'title': 'Cantidad'},
            font={'size': 9},
            height=140,
            dragmode=False,
            margin={'l': 20, 'b': 10, 't': 20, 'r': 10},
            legend={'orientation': "h", 'x': 0, 'y': 0},
            # legend=dict(orientation='h', x=0, y=-0.65),
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Personas Inscritas en Fonasa'
        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_Isapre(df):
        trace1 = go.Scatter(
            x=df['ano'],
            y=df['Isapre'],
            mode='lines+markers',
            name='Isapre',
            line=dict(
                color=('darkred'),
                width=2, ),
        )

        data = [trace1]

        layout = go.Layout(
            xaxis={'tickmode': 'linear', 'tick0': '1'},
            # yaxis={'title': 'Cantidad'},
            font={'size': 9},
            dragmode=False,
            height=130,
            margin={'l': 30, 'b': 10, 't': 20, 'r': 10},
            # legend={'orientation': "h", 'size': '5'},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Personas Inscritas en Isapre'
        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_percepcion(df):
        trace1 = go.Scatter(
            x=df['ano'],
            y=df['comercial'],
            mode='lines+markers',
            name='C.Comerciales',
            line=dict(
                color=('darkred'),
                width=2, ),
        )
        trace2 = go.Scatter(
            x=df['ano'],
            y=df['parques'],
            mode='lines+markers',
            name='Parques',
            line=dict(
                color=('black'),
                width=2, ),
        )
        data = [trace1, trace2]

        layout = go.Layout(
            xaxis={'tickmode': 'linear', 'tick0': '1'},
            yaxis={'title': '%'},
            dragmode=False,
            font={'size': 9},
            height=118,
            margin={'l': 35, 'b': 10, 't': 20, 'r': 10},
            legend=dict(orientation='h', x=0, y=1.1, bgcolor='rgba(0,0,0,0)'),
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Percepción de Seguridad'
        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_tasa(df):
        trace1 = go.Scatter(
            x=df['ano'],
            y=df['Tasa_hurtos'],
            mode='lines+markers',
            name='Tasa_hurtos',
            line=dict(
                color=('darkred'),
                width=2, ),
        )
        data = [trace1]

        layout = go.Layout(
            xaxis={'tickmode': 'linear', 'tick0': '1'},
            # yaxis={'title': 'Cantidad'},
            font={'size': 9},
            dragmode=False,
            height=118,
            margin={'l': 35, 'b': 10, 't': 20, 'r': 10},
            # legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Tasa de hurtos'
        )

        fig = dict(data=data, layout=layout)

        return fig

    df_omil = df_fil[df_fil['Personas_empleo'] > 0]
    omil = figure_omil(df_omil[['id_comuna', 'ano', 'Personas_empleo', 'Personas_capacitacion']])

    df_fuer = df_fil[df_fil['Fuerza_Trabajo'] > 0]
    fuerza = figure_fuerza(df_fuer[['id_comuna', 'ano', 'Fuerza_Trabajo']])

    df_fona = df_fil[df_fil['FONASA_A'] > 0]
    fonasa = figure_fonasa(df_fona[['id_comuna', 'ano', 'FONASA_A', 'FONASA_B', 'FONASA_C', 'FONASA_D']])

    df_isap = df_fil[df_fil['Isapre'] > 0]
    isapre = figure_Isapre(df_isap[['id_comuna', 'ano', 'Isapre']])

    df_tasa = df_fil[df_fil['Tasa_hurtos'] > 0]
    tasa = figure_tasa(df_tasa[['id_comuna', 'ano', 'Tasa_hurtos']])

    df_pers = df_fil[df_fil['comercial'] > 0]
    percepcion = figure_percepcion(df_pers[['id_comuna', 'ano', 'comercial', 'parques']])

    return omil, fuerza, fonasa, isapre, percepcion, tasa


def update_emprendimiento(id_comuna):
    url = 'data/chl/etl_Emprende_2015.csv'  # TODO: API Falta
    col = ['cod_comuna', 'Tramos de edad', 'Programa']
    df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
    df_fil = df.query('cod_comuna == "' + str(id_comuna) + '"')  # .to_dict('records')

    grp_pro = df_fil.groupby('Programa')
    df1 = pd.DataFrame(grp_pro.agg(np.count_nonzero)).reset_index()

    grp_tra = df_fil.groupby('Tramos de edad')
    df2 = pd.DataFrame(grp_tra.agg(np.count_nonzero)).reset_index()

    def figure_emprende(df):
        trace = go.Bar(
            x=df1['cod_comuna'],
            y=df1['Programa'],
            orientation='h',
            marker=dict(
                color=('darkred')),
        )

        data = [trace]

        layout = go.Layout(
            # xaxis={ 'range':[2012, 2019]},
            # yaxis={'title': 'Cantidad'},
            font={'size': 9},
            dragmode=False,
            height=120,
            margin={'l': 40, 'b': 20, 't': 20, 'r': 10},
            legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Programa de Emprendimiento'
        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_etareo(val):
        trace1 = go.Bar(
            x=df2['Tramos de edad'],
            y=df2['cod_comuna'],
            marker=dict(
                color=('darkred', '#657b5b', '#412f55', '#7a7214')),

            # name='Fonasa A',

        )

        data = [trace1]

        layout = go.Layout(
            # xaxis={ 'range':[2012, 2019]},
            # yaxis={'title': 'Cantidad'},
            barmode='stack',
            font={'size': 9},
            dragmode=False,
            height=118,
            margin={'l': 20, 'b': 50, 't': 20, 'r': 10},

            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Grupos Etareos'
        )

        fig = dict(data=data, layout=layout)

        return fig

        emprende = figure_percepcion(df_fil[['id_comuna', 'ano', 'comercial', 'parques']])

    emprende = figure_emprende(df1)

    etareo = figure_etareo(df2)

    return emprende, etareo


def update_pib(id_comuna):
    def region(id=13114):
        url = 'data/chl/etl_geo_datos_mall.csv'  # TODO: API - Falta
        col = ['id_comuna', 'id_region']
        df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
        df_fil = df.query('id_comuna == "' + str(id) + '"')
        val = df_fil.get('id_region').values[0]
        return val

    col = ['cod_region', 'ano', 'pib']
    url = 'data/chl/etl_pib_clio.csv'  # TODO: API Falta
    df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
    df_fil = df.query('cod_region == "' + str(region(id_comuna)) + '"')

    gb = df_fil.groupby('ano')
    df_fil["pib_mean"] = gb["pib"].transform("mean")

    def figure_pib(df):
        trace0 = go.Scatter(
            x=df['ano'],
            y=df['pib_mean'],
            # name='Low 2014',
            line=dict(
                color=('darkred'),
                width=2, ),
            mode='lines+markers',
            opacity=0.7,

        )
        data = [trace0]

        layout = go.Layout(
            xaxis={'tickmode': 'linear', 'tick0': '1'},
            # yaxis={'title': 'Ingreso promedio'},
            dragmode=False,
            height=140,
            font={'size': 9},
            margin={'l': 20, 'b': 10, 't': 20, 'r': 10},
            # legend={'x': 0, 'y': 1},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Producto Interno Bruto'
        )

        fig = dict(data=data, layout=layout)

        return fig

    pib = figure_pib(df_fil)

    return pib


def update_proy_habit(id_comuna):
    url = 'data/chl/etl_proyeccion_hab.csv'  # TODO: API Falta (proyeccion_hab.csv)
    col = ['id_relacion', 'ano', 'total']

    df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
    df_fil = df.query('id_relacion == "' + str(id_comuna) + '"')

    def figure_proy_habit(df):
        trace1 = go.Scatter(
            x=df['ano'],
            y=df['total'],
            mode='lines+markers',
            name='Proyeccion de habitantes',
            line=dict(
                color=('darkred'),
                width=2, ),
        )
        data = [trace1]

        layout = go.Layout(
            xaxis={'tickmode': 'linear', 'tick0': '1'},
            # yaxis={'title': 'Cantidad'},
            dragmode=False,
            font={'size': 9},
            height=140,
            margin={'l': 30, 'b': 10, 't': 20, 'r': 10},
            legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Proyección de Habitantes'
        )

        fig = dict(data=data, layout=layout)

        return fig

    proyeccion = figure_proy_habit(df_fil)

    return proyeccion


def update_censo(id_comuna):
    url_api = "http://18.221.61.6:5000/api/var=censo&comuna=" + str(id_comuna)  # TODO: Como dispongo de los historicos
    col = ['PERSONAS']
    df = pd.read_csv(url_api, usecols=col, delimiter=',', encoding='latin-1')

    tot_pais = 17574003  # TODO: Agregar codigo de total columna
    tot_comuna = df.get('PERSONAS').values[0]

    total_comuna = f"{tot_comuna:,d}"
    porc_hab = "{:.2%}".format(tot_comuna / tot_pais)

    return total_comuna, porc_hab


def update_casen(id_comuna):
    url = 'data/chl/etl_casen_clio.csv'  # TODO: API Falta
    col = ['id_comuna', 'year', 'ytotcor', 'pobreza']
    df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
    df_fil = df.query('id_comuna == "' + str(id_comuna) + '"')

    # df2 = pd.DataFrame(grp_tra.agg(np.count_nonzero)).reset_index()

    df_ing = df_fil.groupby('year').agg(np.average).reset_index()
    df_pob = df_fil.groupby('pobreza').agg(np.count_nonzero).reset_index()

    def figure_ingreso(df):
        trace0 = go.Scatter(
            x=df['year'],
            y=df['ytotcor'],  # .iloc[:, 2],
            # name='Low 2014',
            line=dict(
                color=('darkred'),
                width=2, ),
            mode='lines+markers',
            opacity=0.7,
            # marker={
            #    'size': 15,
            #    'line': {'width': 0.5, 'color': 'white'}
            # },
        )
        data = [trace0]

        layout = go.Layout(
            xaxis={'tickmode': 'linear', 'tick0': '1'},
            # yaxis={'title': 'Ingreso promedio'},
            font={'size': 9},
            dragmode=False,
            height=130,
            margin={'l': 30, 'b': 10, 't': 20, 'r': 10},
            legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Ingreso Promedio familiar',
        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_pobreza(df):
        trace = go.Bar(
            x=df['year'],
            y=df['pobreza'],
            orientation='h',
            marker=dict(
                color=('darkred')),
        )

        data = [trace]

        layout = go.Layout(
            # xaxis={ 'range':[2012, 2019]},
            # yaxis={'title': 'Cantidad'},
            font={'size': 9},
            dragmode=False,
            height=75,
            margin={'l': 100, 'b': 10, 't': 20, 'r': 10},
            legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Nivel de pobreza'
        )

        fig = dict(data=data, layout=layout)

        return fig

    ingreso = figure_ingreso(df_ing)
    pobreza = figure_pobreza(df_pob)
    return pobreza, ingreso


########################################################################################################################
# LAYOUTS
########################################################################################################################

layout = html.Main([
    # Nivel superior
    html.Div([
        # Censo y proyección
        html.Div([
            # Dropdown mall
            html.Div([
                dcc.Dropdown(
                    id='dropdown_malls',
                    className='dropdown menu',
                    options=[{'label': i['name'], 'value': i['id_comuna']} for i in dfs.to_dict(orient='records')],
                    placeholder="Seleccione el Mall",
                    clearable=False,
                    disabled=False,
                    value=13114,

                )
            ], className='bloque'),

            # Graf. Proyección crecimiento de habitantes
            html.Div([
                dcc.Graph(id='habita_graf_proy_chl', config={'displayModeBar': False})
            ], className='bloque'),

            # Indicadores
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(id='nro_habit_chl', style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.Div('Habitantes en la comuna', style={'font-size': '10px'})
                    ], className='bloque-mini')

                ], className='cell small-6'),

                html.Div([
                    html.Div([
                        html.Div(id='por_habit_chl', style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.Div('% de habitantes (nacion)', style={'font-size': '10px'})
                    ], className='bloque-mini')

                ], className='cell small-6')

            ], className='grid-x align-center')

        ], className='cell small-12 medium-6 large-3'),

        # Seccion del empleo
        html.Div([
            # Indicadores OMIL
            html.Div([
                dcc.Graph(id='empleo_graf_omil_chl', config={'displayModeBar': False}),
            ], className='bloque'),

            # Graf. Fuerza productiva
            html.Div([
                dcc.Graph(id='empleo_graf_fuerza_chl', config={'displayModeBar': False}),
            ], className='bloque'),

            # Graf. Indice de pobreza
            html.Div([
                dcc.Graph(id='empleo_graf_pobreza_chl', config={'displayModeBar': False}),
            ], className='bloque'),

        ], className='cell small-12 medium-6 large-3'),

        # Seccion del emprendimiento
        html.Div([
            # Graf. Tipo de emprendimiento
            html.Div([
                dcc.Graph(id='emprend_graf_tipo_chl', config={'displayModeBar': False}),
            ], className='bloque'),

            # Graf. Tramos etareos
            html.Div([
                dcc.Graph(id='emprend_graf_etareos_chl', config={'displayModeBar': False}),
            ], className='bloque')

        ], className='cell small-12 medium-6 large-3'),

        # Seccion del seguridad
        html.Div([
            # Percepción de la seguridad
            html.Div([
                dcc.Graph(id='seguro_graf_percep_chl', config={'displayModeBar': False})
            ], className='bloque'),

            # Graf. Tasa de hurtos
            html.Div([
                dcc.Graph(id='seguro_graf_tasa_chl', config={'displayModeBar': False}),
            ], className='bloque')

        ], className='cell small-12 medium-6 large-3'),
    ], className='grid-x'),

    # Nivel inferior
    html.Div([
        # Ingreso
        html.Div([
            # Graf. Ingreso pib
            html.Div([
                # Graf. Ingreso pib
                dcc.Graph(id='econom_graf_pib_chl', animate=True, config={'displayModeBar': False}),

            ], className='bloque'),

            # Graf. Ingreso promedio familia
            html.Div([
                # Graf. Ingreso promedio familia
                dcc.Graph(id='econom_graf_ingreso_chl', config={'displayModeBar': False})

            ], className='bloque')

        ], className='cell small-12 medium-6 large-3'),

        # Seccion del salud
        html.Div([
            # Graf. Fonasa
            html.Div([
                dcc.Graph(id='salud_graf_fonasa_chl', config={'displayModeBar': False}),
            ], className='bloque'),

            # Graf. Isapre
            html.Div([
                dcc.Graph(id='salud_graf_isapre_chl', config={'displayModeBar': False}),
            ], className='bloque')

        ], className='cell small-12 medium-6 large-3'),

        # Mapa
        html.Div([
            # Mapa
            html.Div([
                html.Div(id='text-content'),
                html.Div([dcc.Graph(id='mapa_box', config={'displayModeBar': False})])
            ], className='bloque')

        ], className='cell small-12 medium-12 large-6'),

    ], className='grid-x')

])


########################################################################################################################
# CALLBACKS
########################################################################################################################

@app.callback(Output('mapa_box', 'figure'), [Input('dropdown_malls', 'value')])
def update_mapa(id_comuna):
    return update_mapbox(id_comuna)


# Fuente Sensacion
@app.callback(
    [Output('empleo_graf_omil_chl', 'figure'), Output('empleo_graf_fuerza_chl', 'figure'),
     Output('salud_graf_fonasa_chl', 'figure'), Output('salud_graf_isapre_chl', 'figure'),
     Output('seguro_graf_percep_chl', 'figure'), Output('seguro_graf_tasa_chl', 'figure')],
    [Input('dropdown_malls', 'value')]
)
def update_content(id_comuna):
    return [i for i in update_sensacion(id_comuna)]


# Fuente Emprendimiento
@app.callback(
    [Output('emprend_graf_tipo_chl', 'figure'), Output('emprend_graf_etareos_chl', 'figure')],
    [Input('dropdown_malls', 'value')]
)
def update_content(id_comuna):
    return [i for i in update_emprendimiento(id_comuna)]


# Fuente PIB
@app.callback(Output('econom_graf_pib_chl', 'figure'), [Input('dropdown_malls', 'value')])
# @cache.memoize(10)
def update_content(id_comuna):
    return update_pib(id_comuna)


# Fuente Proyeccion
@app.callback(Output('habita_graf_proy_chl', 'figure'), [Input('dropdown_malls', 'value')])
def update_content(id_comuna):
    return update_proy_habit(id_comuna)


# Fuente API-Censo
@app.callback([Output('nro_habit_chl', 'children'), Output('por_habit_chl', 'children')],
              [Input('dropdown_malls', 'value')])
def update(id_comuna):
    return [str(i) for i in update_censo(id_comuna)]


# Fuente Casen
@app.callback([Output('empleo_graf_pobreza_chl', 'figure'), Output('econom_graf_ingreso_chl', 'figure')],
              [Input('dropdown_malls', 'value')]
              )
def update(id_comuna):
    return [i for i in update_casen(id_comuna)]


# Visualiza datos de los points (Que estudian)
@app.callback(Output('text-content', 'children'), [Input('mapa_box', 'hoverData')])
def show_carreras(hoverData):
    if hoverData != None:
        url = 'data/chl/etl_carreras.csv'
        df = pd.read_csv(url, delimiter=';', encoding='latin-1')
        s = df[df['rbd'] == hoverData['points'][0]['customdata']]
        ss = s.groupby('carrera')
        df1 = pd.DataFrame(ss.agg(np.count_nonzero)).reset_index().head(5)

        lista = str(df1['carrera'].to_list())[1:-1]

    else:
        lista = ''

    return html.Label([lista], className='primary label')
