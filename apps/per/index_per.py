import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from components.functions import update_mapbox_per
import plotly.graph_objs as go
from app import app
import numpy as np
import pandas as pd

########################################################################################################################
# FUNTIONS
########################################################################################################################
columna = ['name', 'pais_iso3', 'id_comuna', 'id_region', 'classification']
df = pd.read_csv('data/per/etl_geo_datos_all.csv', usecols=columna, delimiter=';', encoding='latin-1')
dfs = df[(df.pais_iso3 == 'PER') & (df.classification == 'Mall')]

def update_casen(id_comuna):
    def region(id):
        columna = ['name', 'pais_iso3', 'id_comuna', 'id_region', 'classification']
        df = pd.read_csv('data/col/etl_geo_datos_all.csv', usecols=columna, delimiter=';', encoding='latin-1')
        dfs = df[(df.pais_iso3 == 'COL') & (df.id_comuna == id)]

        reg = int(dfs.get('id_region').values[0])

        return reg

    url = 'data/per/etl_casen_per.csv'  # TODO: API Falta
    col = ['ubigeo', 'ano', 'ytocoh', 'pobreza']
    df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
    df_fil = df.query('ubigeo == "' + str(id_comuna) + '"')

    # df2 = pd.DataFrame(grp_tra.agg(np.count_nonzero)).reset_index()

    df_ing = df_fil.groupby('ano').agg(np.average).reset_index()
    df_pob = df_fil.groupby('pobreza').agg(np.sum).reset_index()

    def figure_ingreso(df):
        trace0 = go.Scatter(
            x=df['ano'],
            y=df['ytocoh'],  # .iloc[:, 2],
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
            #yaxis={'title': 'Ingreso promedio'},
            font={'size': 10},
            height=133,
            dragmode=False,
            margin={'l': 40, 'b': 20, 't': 20, 'r': 10},
            legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Ingreso Promedio por Familia',
        )

        fig = dict(data=data, layout=layout)

        return fig

    def figure_pobreza(df):

        trace = go.Bar(
            x=df['ano'],
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
            height=135,
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

def update_censo(id_comuna):
    df = pd.read_csv('data/per/proyeccion_hab_per.csv', delimiter=';', encoding='latin-1')
    df_proy = df[(df.id_dpto == id_comuna)]

    df_year = df[(df.id_dpto == id_comuna) & (df.year == 2015)]

    tot_pais = 32162184  # TODO: Agregar codigo de total columna
    tot_comuna = df_year.get('cant').values[0]

    total_comuna = f"{tot_comuna:,d}"
    porc_hab = "{:.2%}".format(tot_comuna / tot_pais)


    def figure_proy(df):
        trace0 = go.Scatter(
            x=df['year'],
            y=df['cant'],  # .iloc[:, 2],
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
            # yaxis={'title': 'Cantidad'},
            dragmode=False,
            font={'size': 9},
            height=170,
            margin={'l': 30, 'b': 25, 't': 20, 'r': 10},
            legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Proyección de Habitantes'
        )

        fig = dict(data=data, layout=layout)

        return fig

    figure = figure_proy(df_proy)

    return figure

########################################################################################################################
# LAYOUTS
########################################################################################################################

layout = html.Main([
    html.Div([
        # Ingreso
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
                    value=150122,

                )
            ], className='bloque'),

            # Graf. Proyección crecimiento de habitantes
            html.Div([
                dcc.Graph(id='habita_graf_proy_per', config={'displayModeBar': False})
            ], className='bloque'),

            # Indicadores
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(id='nro_habit_per', style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.Div('Habitantes en el municipio', style={'font-size': '10px'})
                    ], className='bloque-mini')

                ], className='cell small-6'),

                html.Div([
                    html.Div([
                        html.Div(id='por_habit_per', style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.Div('% de habitantes (nacion)', style={'font-size': '10px'})
                    ], className='bloque-mini')

                ], className='cell small-6')

            ], className='grid-x align-center')
        ], className='cell small-12 medium-6 large-3'),

        # Seccion del salud
        html.Div([

            # Graf. Ingreso pib
            html.Div([
                dcc.Graph(id='econom_graf_ingreso_per', config={'displayModeBar': False})
            ], className='bloque'),

            # Graf. Indice de pobreza
            html.Div([
                dcc.Graph(id='empleo_graf_pobreza_per', config={'displayModeBar': False}),
            ], className='bloque'),

        ], className='cell small-12 medium-6 large-3'),

        # Mapa
        html.Div([
            html.Div([
                html.Div([dcc.Graph(id='mapa_box_per', config={'displayModeBar': False})])
            ], className='bloque')

        ], className='cell small-12 medium-12 large-6'),

    ], className='grid-x nivel')

])

########################################################################################################################
# CALLBACKS
########################################################################################################################

@app.callback(Output('mapa_box_per', 'figure'), [Input('dropdown_malls', 'value')])
def update_mapa(id_comuna):
    return update_mapbox_per(id_comuna)

# Fuente Casen
@app.callback([Output('empleo_graf_pobreza_per', 'figure'), Output('econom_graf_ingreso_per', 'figure')],
    [Input('dropdown_malls', 'value')]
)
def update(id_comuna):
    return [i for i in update_casen(id_comuna)]


@app.callback(Output('habita_graf_proy_per', 'figure'),
              [Input('dropdown_malls', 'value')])
def update_mapa(id_comuna):
    columna = ['name', 'pais_iso3', 'id_comuna', 'id_region', 'classification']
    df = pd.read_csv('data/per/etl_geo_datos_all.csv', usecols=columna, delimiter=';', encoding='latin-1')
    dfs = df[(df.pais_iso3 == 'PER') & (df.classification == 'Mall') & (df.id_comuna == id_comuna)]

    tot = dfs.get('id_region').values[0]

    return update_censo(tot)