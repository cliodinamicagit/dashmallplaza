import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from components.functions import update_mapbox_col
import plotly.graph_objs as go
from app import app
import numpy as np
import pandas as pd

########################################################################################################################
# FUNTIONS
########################################################################################################################
columna = ['name', 'pais_iso3', 'id_comuna', 'id_region', 'classification']
df = pd.read_csv('data/col/etl_geo_datos_all.csv', usecols=columna, delimiter=';', encoding='latin-1')
dfs = df[(df.pais_iso3 == 'COL') & (df.classification == 'Mall')]



def update_casen(id_comuna):
    def region(id):
        columna = ['name', 'pais_iso3', 'id_comuna', 'id_region', 'classification']
        df = pd.read_csv('data/col/etl_geo_datos_all.csv', usecols=columna, delimiter=';', encoding='latin-1')
        dfs = df[(df.pais_iso3 == 'COL') & (df.id_comuna == id)]

        reg = int(dfs.get('id_region').values[0])

        return reg


    url = 'data/col/etl_casen_col.csv'  # TODO: API Falta
    col = ['dpto', 'year', 'yto_he', 'pobreza']
    df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
    df_fil = df.query('dpto == "' + str(region(id_comuna)) + '"')

    # df2 = pd.DataFrame(grp_tra.agg(np.count_nonzero)).reset_index()

    df_ing = df_fil.groupby('year').agg(np.average).reset_index()
    df_pob = df_fil.groupby('pobreza').agg(np.count_nonzero).reset_index()

    def figure_ingreso(df):
        trace0 = go.Scatter(
            x=df['year'],
            y=df['yto_he'],  # .iloc[:, 2],
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
    columna = ['DPMP', 'year', 'total']
    df = pd.read_csv('data/col/etl_proyeccion_hab_col.csv', usecols=columna, delimiter=';', encoding='latin-1')
    df_proy = df[(df.DPMP == id_comuna)]

    df_year = df[(df.DPMP == id_comuna) & (df.year == 2017)]

    tot_pais = 48258494  # TODO: Agregar codigo de total columna
    tot_comuna = df_year.get('total').values[0]

    total_comuna = f"{tot_comuna:,d}"
    porc_hab = "{:.2%}".format(tot_comuna / tot_pais)


    def figure_proy(df):
        trace0 = go.Scatter(
            x=df['year'],
            y=df['total'],  # .iloc[:, 2],
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
            margin={'l': 30, 'b': 10, 't': 20, 'r': 10},
            legend={'orientation': "h"},
            hovermode='closest',
            paper_bgcolor='#f9f9f9',
            plot_bgcolor='#f9f9f9',
            title='Proyección de Habitantes'
        )

        fig = dict(data=data, layout=layout)

        return fig

    figure = figure_proy(df_proy)

    return str(total_comuna), str(porc_hab), figure

########################################################################################################################
# LAYOUTS
########################################################################################################################

layout = html.Main([


    # Nivel inferior
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
                    value=13001,

                )
            ], className='bloque'),

            # Graf. Proyección crecimiento de habitantes
            html.Div([
                dcc.Graph(id='habita_graf_proy_col', config={'displayModeBar': False})
            ], className='bloque'),

            # Indicadores
            html.Div([
                html.Div([
                    html.Div([
                        html.Div(id='nro_habit_col', style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.Div('Habitantes en el municipio', style={'font-size': '10px'})
                    ], className='bloque-mini')

                ], className='cell small-6'),

                html.Div([
                    html.Div([
                        html.Div(id='por_habit_col', style={'font-size': '18px', 'font-weight': 'bold'}),
                        html.Div('% de habitantes (nacion)', style={'font-size': '10px'})
                    ], className='bloque-mini')

                ], className='cell small-6')

            ], className='grid-x align-center')

        ], className='cell small-12 medium-6 large-3'),

        # Seccion del salud
        html.Div([

            # Graf. Ingreso pib
            html.Div([
                dcc.Graph(id='econom_graf_ingreso_col', config={'displayModeBar': False})
            ], className='bloque'),

            # Graf. Indice de pobreza
            html.Div([
                dcc.Graph(id='empleo_graf_pobreza_col', config={'displayModeBar': False}),
            ], className='bloque'),

        ], className='cell small-12 medium-6 large-3'),

        # Mapa
        html.Div([
            html.Div([
                html.Div([dcc.Graph(id='mapa_box_col', config={'displayModeBar': False})])
            ], className='bloque')

        ], className='cell small-12 medium-12 large-6'),

    ], className='grid-x nivel')

])

########################################################################################################################
# CALLBACKS
########################################################################################################################

@app.callback(Output('mapa_box_col', 'figure'), [Input('dropdown_malls', 'value')])
def update_mapa(id_comuna):
    return update_mapbox_col(id_comuna)


# Fuente Casen
@app.callback([Output('empleo_graf_pobreza_col', 'figure'), Output('econom_graf_ingreso_col', 'figure')],
    [Input('dropdown_malls', 'value')]
)
def update(id_comuna):
    return [i for i in update_casen(id_comuna)]


@app.callback([Output('nro_habit_col', 'children'), Output('por_habit_col', 'children'),
               Output('habita_graf_proy_col', 'figure')],
              [Input('dropdown_malls', 'value')])
def update_mapa(id_comuna):
    return [i for i in update_censo(id_comuna)]