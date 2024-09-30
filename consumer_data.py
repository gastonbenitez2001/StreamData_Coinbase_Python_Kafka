import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from biblioteca import ClasePrueba

# === VAR DE DASH

# Instancia de prueba
instancia = ClasePrueba()

# Crear una aplicación Dash
app = dash.Dash(__name__)

# LAYOUT APP

app.layout = html.Div(children=[
    html.H1(children='Gráfico de Burbujas de Criptomonedas'),

    # Gráfico de burbujas
    dcc.Graph(id='crypto_sizes'),

    #capital
    dcc.Graph(id="capital"),

    # Intervalo de tiempo
    dcc.Interval(
        id='interval_time',
        interval=5 * 1000,  # Actualizar cada 5 segundos
        n_intervals=0
    ),

    # Componente para almacenar datos temporalmente
    dcc.Store(id='dummy-store')
])


# Callback que se ejecuta cada 5 segundos
@app.callback(
    Output('crypto_sizes', 'figure'),  # Output: El gráfico de burbujas
    Input('interval_time', 'n_intervals')  # Input: Cada 5 segundos
)
def update_graph(n_intervals):
    
    instancia.update_vars()

    # Crear el gráfico basado en los datos almacenados
    figure = {
        'data': [
            {'x': ['BTC', 'ETH'], 'y': [instancia.btc_size,instancia.eth_size], 'type': 'bar'}
        ],
        'layout': {
            'title': 'Capital Transaccionado de Criptomonedas'
        }
    }
    return figure

    

# Ejecutar la aplicación en el servidor local
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
