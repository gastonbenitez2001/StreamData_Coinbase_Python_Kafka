import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from biblioteca import CryptoConsumer

# === VAR TO DASH

# Create instance
instancia = CryptoConsumer()

#Create dash app
app = dash.Dash(__name__)

# LAYOUT APP

app.layout = html.Div(children=[
    html.H1(children='Gráfico de Burbujas de Criptomonedas'),

    #Figure
    dcc.Graph(id='crypto_sizes'),

    #capital
    dcc.Graph(id="capital"),

    # Intervalo de tiempo
    dcc.Interval(
        id='interval_time',
        interval=5 * 1000,  # update for each 5 seconds
        n_intervals=0
    )
])


#Execute callback for each 5 seconds
@app.callback(
    [Output('crypto_sizes', 'figure'),  # Primer gráfico
     Output('capital', 'figure')],  # Segundo gráfico
    [Input('interval_time', 'n_intervals')]  # Input: Cada 5 segundos
)
def update_graph(n_intervals):

    print(".")
    
    instancia.update_vars()

    print(instancia.eth_size,instancia.btc_size,instancia.eth_capital,instancia.btc_capital)

    #Create and send figure number of cryptocurrencies transferred
    figure_sizes = {
        'data': [
            {'x': ['BTC', 'ETH'], 'y': [instancia.btc_size,instancia.eth_size], 'type': 'bar'}
        ],
        'layout': {
            'title': 'Total number of cryptocurrencies transferred'
        }
    }



    #Create cryptocurrencies transferred figure
    figure_capital = {
        'data': [
            {'x': ['BTC', 'ETH'], 'y': [instancia.btc_capital,instancia.eth_capital], 'type': 'bar'}
        ],
        'layout': {
            'title': 'Capital cryptocurrencies transferred '
        }
    }




    return figure_sizes, figure_capital


if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
