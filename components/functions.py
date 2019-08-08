import pandas as pd
import os

########################################################################################################################
mapbox_access_token2 = 'pk.eyJ1IjoiZmFycmVkb25kbyIsImEiOiJjanc2ZnR2MjMxOW42NDFvdzJpZG5haDhiIn0.xGE3lzz9LPPcppdn03eeeQ'
mapbox_access_token ='pk.eyJ1IjoiZmFycmVkb25kbyIsImEiOiJjanc2ZnR2MjMxOW42NDFvdzJpZG5haDhiIn0.xGE3lzz9LPPcppdn03eeeQ'

synbol = ['airfield', 'airport', 'alcohol-shop', 'amusement-park', 'aquarium', 'art-gallery', 'attraction', 'bakery',
          'bank', 'bar', 'beer', 'bicycle', 'bicycle-share', 'bus', 'cafe', 'campsite', 'car', 'castle', 'cemetery',
          'cinema', 'circle', 'circle-stroked', 'clothing-store', 'college', 'dentist', 'doctor', 'dog-park',
          'drinking-water', 'embassy', 'entrance', 'fast-food', 'ferry', 'fire-station', 'fuel', 'garden', 'golf',
          'grocery', 'harbor', 'heliport', 'hospital', 'ice-cream', 'information', 'laundry', 'library', 'lodging',
          'marker', 'monument', 'mountain', 'museum', 'music', 'park', 'pharmacy', 'picnic-site', 'place-of-worship',
          'playground', 'police', 'post', 'prison', 'rail', 'rail-light', 'rail-metro', 'religious-christian',
          'religious-jewish', 'religious-muslim', 'restaurant', 'rocket', 'school', 'shop', 'stadium', 'star',
          'suitcase', 'swimming', 'theatre', 'toilet', 'town-hall', 'triangle', 'triangle-stroked', 'veterinary',
          'volcano', 'zoo']
# TODO:
def update_mapbox(id_comuna):

    def coor_malls():  # TODO: por ahora el id es la comuna, arreglar
        url = 'data/gral/etl_geo_datos_mall.csv'
        col = ['id_comuna', 'lat', 'lng', 'id_mall']
        df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
        # df_fil = df[df['id_comuna'][0] == str(id_comuna)]
        df_fil = df.query('id_comuna == "' + str(id_comuna) + '"')

        lat = round(float(df_fil.get('lat').values[0]), 6)
        lng = round(float(df_fil.get('lng').values[0]), 6)
        mall_id = float(df_fil.get('id_mall').values[0])

        return lat, lng, mall_id

    def ld(fn):
        return dict(
            sourcetype='geojson',
            source=f'https://raw.githubusercontent.com/sergiolucero/data/master/GEO/here.com/{fn[0]}',
            type='fill', color=fn[1]
        )

    fns = [(f'amall_{(int(coor_malls()[2]))}_min_5.json', 'rgba(255,0,0,0.1)'),
           (f'amall_{(int(coor_malls()[2]))}_min_10.json', 'rgba(0,255,0,0.1)'),
           (f'amall_{(int(coor_malls()[2]))}_min_20.json', 'rgba(0,0,255,0.1)'),
           ]

    url = 'data/gral/etl_geo_datos_all.csv'
    df = pd.read_csv(url, delimiter=';', encoding='latin-1')
    clas = df[["classification"]].drop_duplicates()

    traces = []

    for clas, i in df.groupby('classification'):
        trace = dict(
            type='scattermapbox',
            name=clas,
            text=[x for x in i['name']],
            lat=[round(x, 6) for x in i['lat']],
            lon=[round(x, 6) for x in i['lng']],
            mode='markers',
            overinfo='text',
            marker=dict(
                symbol=synbol[20],
                size=i['size']*0.6,
                opacity=0.8,
                color=i['color']),
            customdata=i['id_mall'],
        )
        traces.append(trace)

    return dict(
        data=traces,
        layout=dict(
            autosize=True,
            height=280,
            margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
            hovermode='closest',
            #legend=dict(orientation='v', x=0, y=0.1, bgcolor='rgba(0,0,0,0)'),
            legend={'orientation': "h", "showlegend": True, 'bgcolor':'rgba(0,0,0,0)'},
            mapbox=dict(
                accesstoken=mapbox_access_token,  # os.environ.get("MAPBOX_KEY"),
                bearing=0,
                center=dict(lat=coor_malls()[0], lon=coor_malls()[1]),
                pitch=10,
                zoom=13,
                style='light',
                layers=[ld(fn) for fn in fns],
                #legend=dict(orientation='h', x=0, y=0.1, bgcolor='rgba(0,0,0,0)'),
            ),
        ),
    )

def update_mapbox_col(id_comuna):

    def coor_malls():  # TODO: por ahora el id es la comuna, arreglar
        url = 'data/gral/etl_geo_datos_mall.csv'
        col = ['id_comuna', 'lat', 'lng', 'id_mall']
        df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
        # df_fil = df[df['id_comuna'][0] == str(id_comuna)]
        df_fil = df.query('id_comuna == "' + str(id_comuna) + '"')

        lat = round(float(df_fil.get('lat').values[0]), 6)
        lng = round(float(df_fil.get('lng').values[0]), 6)
        mall_id = float(df_fil.get('id_mall').values[0])

        return lat, lng, mall_id

    def ld(fn):
        return dict(
            sourcetype='geojson',
            source=f'https://raw.githubusercontent.com/sergiolucero/data/master/GEO/here.com/{fn[0]}',
            type='fill', color=fn[1]
        )

    fns = [(f'amall_{(int(coor_malls()[2]))}_min_5.json', 'rgba(255,0,0,0.1)'),
           (f'amall_{(int(coor_malls()[2]))}_min_10.json', 'rgba(0,255,0,0.1)'),
           (f'amall_{(int(coor_malls()[2]))}_min_20.json', 'rgba(0,0,255,0.1)')]


    url = 'data/gral/etl_geo_datos_all.csv'
    df = pd.read_csv(url, delimiter=';', encoding='latin-1')
    clas = df[["classification"]].drop_duplicates()

    traces = []

    for clas, i in df.groupby('classification'):
        trace = dict(
            type='scattermapbox',
            name=clas,

            text=[x for x in i['name']],
            lat=[round(x, 6) for x in i['lat']],
            lon=[round(x, 6) for x in i['lng']],
            mode='markers',
            marker=dict(
                symbol=synbol[20],
                size=i['size']*0.6,
                opacity=0.8,
                color=i['color'])
        )
        traces.append(trace)

    return dict(
        data=traces,
        layout=dict(
            autosize=True,
            height=280,
            margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
            hovermode='closest',
            legend={'orientation': "h", "showlegend": True},
            mapbox=dict(
                accesstoken=mapbox_access_token,  # os.environ.get("MAPBOX_KEY"),
                bearing=0,
                center=dict(lat=coor_malls()[0], lon=coor_malls()[1]),
                pitch=10,
                zoom=13,
                style='light',
                layers=[ld(fn) for fn in fns],

            )
        )
    )

def update_mapbox_per(id_comuna):

    def coor_malls():  # TODO: por ahora el id es la comuna, arreglar
        url = 'data/per/etl_geo_datos_all.csv'
        col = ['id_comuna', 'lat', 'lng', 'id_mall']
        df = pd.read_csv(url, usecols=col, delimiter=';', encoding='latin-1')
        # df_fil = df[df['id_comuna'][0] == str(id_comuna)]
        df_fil = df.query('id_comuna == "' + str(id_comuna) + '"')

        lat = round(float(df_fil.get('lat').values[0]), 6)
        lng = round(float(df_fil.get('lng').values[0]), 6)
        mall_id = float(df_fil.get('id_mall').values[0])

        return lat, lng, mall_id

    def ld(fn):
        return dict(
            sourcetype='geojson',
            source=f'https://raw.githubusercontent.com/sergiolucero/data/master/GEO/here.com/{fn[0]}',
            type='fill', color=fn[1]
        )

    fns = [(f'amall_{(int(coor_malls()[2]))}_min_5.json', 'rgba(255,0,0,0.1)'),
           (f'amall_{(int(coor_malls()[2]))}_min_10.json', 'rgba(0,255,0,0.1)'),
           (f'amall_{(int(coor_malls()[2]))}_min_20.json', 'rgba(0,0,255,0.1)')]



    url = 'data/gral/etl_geo_datos_all.csv'
    df = pd.read_csv(url, delimiter=';', encoding='latin-1')
    clas = df[["classification"]].drop_duplicates()




    traces = []

    for clas, i in df.groupby('classification'):
        trace = dict(
            type='scattermapbox',
            name=clas,

            text=[x for x in i['name']],
            lat=[round(x, 6) for x in i['lat']],
            lon=[round(x, 6) for x in i['lng']],
            mode='markers',
            marker=dict(
                symbol=synbol[20],
                size=i['size']*0.6,
                opacity=0.8,
                color=i['color'])
        )
        traces.append(trace)

    return dict(
        data=traces,
        layout=dict(
            autosize=True,
            height=280,
            margin={'l': 0, 'b': 0, 't': 0, 'r': 0},
            hovermode='closest',
            legend={'orientation': "h", "showlegend": True},
            mapbox=dict(
                accesstoken=mapbox_access_token,  # os.environ.get("MAPBOX_KEY"),
                bearing=0,
                center=dict(lat=coor_malls()[0], lon=coor_malls()[1]),
                pitch=10,
                zoom=13,
                style='light',
                layers=[ld(fn) for fn in fns],

            )
        )
    )


