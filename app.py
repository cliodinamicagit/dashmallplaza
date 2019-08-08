import dash
import dash_auth

external_stylesheets1 = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# external JavaScript files
external_scripts = [
    # Mapbox
    {
        'src':'https://api.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.js'
    },
    {'src': 'https://api.tiles.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.js'},
    # Foundation
    {
        'src': 'https://cdn.jsdelivr.net/npm/foundation-sites@6.5.3/dist/js/foundation.min.js',
        'integrity': 'sha256-/PFxCnsMh+nTuM0k3VJCRch1gwnCfKjaP8rJNq5SoBg= sha384-9ksAFjQjZnpqt6VtpjMjlp2S0qrGbcwF/rvrLUg2vciMhwc1UJJeAAOLuJ96w+Nj sha512-UMSn6RHqqJeJcIfV1eS2tPKCjzaHkU/KqgAnQ7Nzn0mLicFxaVhm9vq7zG5+0LALt15j1ljlg8Fp9PT1VGNmDw==',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    },
    {
        'src': "https://code.jquery.com/jquery-3.3.1.slim.min.js",
        'integrity': "sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo",
        'crossorigin': "anonymous"
    },
    {
        'src': "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js",
        'integrity': "sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1",
        'crossorigin': "anonymous"
    },
    {
        'src': "https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js",
        'integrity': "sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM",
        'crossorigin': "anonymous"
    },
]

# external CSS stylesheets
external_stylesheets = [
    # Flexbox
    'https://codepen.io/chriddyp/pen/bWLwgP.css',
    # Mapbox
    'https://api.mapbox.com/mapbox-gl-js/v1.1.1/mapbox-gl.css'
    # Foundation
    #'https://dhbhdrzi4tiry.cloudfront.net/cdn/sites/foundation.min.css',
]

########################################################################################################################
# APP
########################################################################################################################

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets,
                meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}]
                )
app.title = "MallPlaza Latinoamerica"

VALID_USERNAME_PASSWORD_PAIRS = {'clio': 'dinamica'}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)
server = app.server
app.config.suppress_callback_exceptions = True