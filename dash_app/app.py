# -*- coding: utf-8 -*-
import sys
print("Python utilisé :", sys.executable)

import dash
from dash import html,dcc, Input, Output
import logging
import plotly.express as px



_logger = logging.getLogger(__name__)

def create_dash_app():
    
    """Créer et configurer l'application Dash"""
    app = dash.Dash(
        __name__,
        requests_pathname_prefix='/dash/',  # Corrige les erreurs de chemin derrière Nginx
        routes_pathname_prefix='/dash/',    # Corrige le loading infini
        assets_url_path='/dash/assets'      # Corrige le chargement des fichiers statiques
    )

    

    # Layout simple
    app.layout = html.Div([
    html.H4('Analysis of the restaurant sales',className='bg-primary'),
    dcc.Graph(id="graph"),
    html.P("Names:"),
    dcc.Dropdown(id='names',
        options=['smoker', 'day', 'time', 'sex'],
        value='day', clearable=False
    ),
    html.P("Values:"),
    dcc.Dropdown(id='values',
        options=['total_bill', 'tip', 'size'],
        value='total_bill', clearable=False
    ),
   ])
    
    @app.callback(
      Output("graph", "figure"),
      Input("names", "value"),
      Input("values", "value"))
    
    def generate_chart(names, values):
      df = px.data.tips() # replace with your own data source
      fig = px.pie(df, values=values, names=names, hole=.3)
      return fig

    return app

# Démarrage de l'application
if __name__ == '__main__':
    app = create_dash_app()
    app.run(debug=True, host='127.0.0.1', port=8050, dev_tools_ui=True)