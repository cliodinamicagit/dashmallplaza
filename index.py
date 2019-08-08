from app import app
import dash_html_components as html

from components.header import Header
from components.footer import Footer

# from apps import app_col, app_chile, app_per
# from dash.dependencies import Input, Output

# see https://dash.plot.ly/external-resources to alter header, footer and favicon
app.index_string = ''' 
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

########################################################################################################################
# LAYOUTS
########################################################################################################################


layout = html.Div([
    Header(),
    html.Main([], id='page-content'),
    Footer()
], id='contenido', className='grid-container fluid')

app.layout = layout

if __name__ == '__main__':
    #app.run_server(debug=True, port=8010)
    app.run_server(debug=True, port=8010, host='0.0.0.0')
