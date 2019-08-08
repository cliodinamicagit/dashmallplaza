import pandas as pd
import numpy as np
import dash_html_components as html
import dash_core_components as dcc

clio_aws_S3 = 'https://cliodina.s3.us-east-2.amazonaws.com/'

url = 'D:/Dropbox/A_Trabajo/Cliodinamica/AWS/data/002_casen/col/col15/col15n.dta'
df = pd.read_stata(url)

print(df.head())





#s.set_index(['CÓDIGO DE INSTITUCIÓN', 'NOMBRE CARRERA']).count(level="NOMBRE CARRERA")

if hoverData['points'][0]['marker.color'] == 'blue' & hoverData['points'][0]['customdata'] > 0:
    url = 'data/chl/etl_carreras.csv'

    df = pd.read_csv(url, delimiter=';', encoding='latin-1')

    s = df[df['rbd'] == hoverData['points'][0]['customdata']]

    ss = s.groupby('carrera')
    df1 = pd.DataFrame(ss.agg(np.count_nonzero)).reset_index().head(5)
    y = html.Label([str(df1['carrera'].to_list())[1:-1]], className='primary label')

else:
    y = ''





