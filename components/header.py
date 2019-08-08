import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from apps.chl import index_chl
from apps.col import index_col
from apps.per import index_per

from app import app
import pandas as pd

from apps.chl import index_chl

########################################################################################################################
def Header():
    columna = ['pais', 'pais_iso3']
    df = pd.read_csv('data/gral/etl_cut_con_paises.csv', usecols=columna, delimiter=';',
                     encoding='latin-1').drop_duplicates()

    return html.Header([
        # Menu
        html.Nav([

            dcc.Dropdown(
                id='dropdown_pais',
                className='dropdown menu',
                options=[{'label': i['pais'], 'value': i['pais_iso3']} for i in df.to_dict(orient='records')],
                placeholder="Seleccione el Pais",
                clearable=False,
                disabled=False,
                value='CHL',
                style={
                    'padding-top': '6px',
                    'padding-left': '2px',
                    'font-size': 'medium'
                }

            )

        ], className='cell small-8 medium-8 large-10 top-bar-left'),

        # Logo
        html.Div([
                html.Img(id='id_img', src="assets/img/logo-clio-consulting-blanco.png", className='align-right', style={
                    'height': '1.5cm',
                    'width': 'auto',
                    'float': 'right',
                    'position': 'relative',
                    'margin-top': 4,
                    'margin-right': 4,
                    'vertical-align': 'middle'
                })
            ], className='cell small-4 medium-4 large-2 top-bar-right'),




    ], id='id_header', className='grid-x grid-padding-x')


########################################################################################################################
# CALLBACKS
########################################################################################################################

@app.callback(
    Output('page-content', 'children'),
    [Input('dropdown_pais', 'value')]
)
def page_content(pais):
    # Establece el layout a mostrar por pais
    children = {'CHL': index_chl.layout, 'COL': index_col.layout, 'PER': index_per.layout}
    return children[pais]