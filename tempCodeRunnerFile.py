from dash import Dash, dcc, html, Output
import plotly.express as px
import pandas as pd
import requests

# Fetch arbitrage opportunities from APIs
def fetch_arbitrage_data():
    # Fetch data from Kucoin and Zebpay APIs
    kucoin_response = requests.get("https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=XRP-USDT")
    zebpay_response = requests.get("https://www.zebapi.com/pro/v1/market/XRP-INR/ticker")
    
    # Process response data
    kucoin_data = kucoin_response.json()
    zebpay_data = zebpay_response.json()
    
    # Extract relevant information for arbitrage calculation
    kucoin_price = float(kucoin_data['data']['price'])
    zebpay_price = float(zebpay_data['market'])
    
    # Calculate arbitrage opportunity
    arbitrage_opportunity = zebpay_price - kucoin_price
    
    return arbitrage_opportunity

# Create Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H4('Cryptocurrency Arbitrage Opportunities'),
    dcc.Graph(id="crypto-arbitrage-graph"),
    html.Hr(),
    html.Div(id='top-opportunity-output'),
    html.Hr(),
    html.H4('Current Prices on Exchanges'),
    html.Div([
        html.Label('Kucoin Price:'),
        html.Div(id='kucoin-price')
    ]),
    html.Div([
        html.Label('Zebpay Price:'),
        html.Div(id='zebpay-price')
    ])
])

# Callback to update graph with real-time data
@app.callback(
    Output("crypto-arbitrage-graph", "figure"), 
    []
)
def display_arbitrage_data():
    arbitrage_opportunity = fetch_arbitrage_data()
    
    fig = px.bar(
        pd.DataFrame({"Arbitrage_Opportunity": [arbitrage_opportunity]}), 
        y="Arbitrage_Opportunity", 
        color="Arbitrage_Opportunity"
    )
    fig.update_layout(title="Real-time Cryptocurrency Arbitrage Opportunities", yaxis_title="Arbitrage Opportunity")
    return fig

# Callback to print top opportunity
@app.callback(
    Output("top-opportunity-output", "children"), 
    []
)
def print_top_opportunity():
    opportunity = fetch_arbitrage_data()
    return f"The current arbitrage opportunity is {opportunity}"

# Callback to update Kucoin price
@app.callback(
    Output("kucoin-price", "children"),
    []
)
def update_kucoin_price():
    kucoin_price = fetch_kucoin_price()  # Fetch current price from API
    return f"${kucoin_price:.2f}"

# Callback to update Zebpay price
@app.callback(
    Output("zebpay-price", "children"),
    []
)
def update_zebpay_price():
    zebpay_price = fetch_zebpay_price()  # Fetch current price from API
    return f"${zebpay_price:.2f}"

if __name__ == "__main__":
    app.run_server(debug=True)
