from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import random

# Step 1: Fetch Data (Mock Data for demonstration)
crypto_data = {
    "Cryptocurrency": ["BTC", "ETH", "XRP", "LTC", "BCH", "EOS", "XLM", "TRX", "ADA", "XMR"],
    "Arbitrage_Opportunity": [0.05, 0.03, 0.07, 0.02, 0.06, 0.04, 0.08, 0.01, 0.09, 0.05] 
}

df = pd.DataFrame(crypto_data)

# Step 2: Calculate Arbitrage Opportunities
df["Arbitrage_Opportunity"] = [random.uniform(5, 10) for _ in range(len(df))]

# Step 3: Sort Data
def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = arr[:mid]
    right = arr[mid:]
    
    left = merge_sort(left)
    right = merge_sort(right)
    
    return merge(left, right)

def merge(left, right):
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    while i < len(left):
        result.append(left[i])
        i += 1
    
    while j < len(right):
        result.append(right[j])
        j += 1
    
    return result

sorted_df = df.sort_values(by="Arbitrage_Opportunity", ascending=False)
sorted_data = merge_sort(sorted_df["Arbitrage_Opportunity"].tolist())
sorted_df["Arbitrage_Opportunity"] = sorted_data

# Step 4: Create Dash App
app = Dash(__name__)

# Step 5: Define Dash Layout
app.layout = html.Div([
    html.H4('Cryptocurrency Arbitrage Opportunities'),
    dcc.Graph(id="crypto-arbitrage-graph"),
    html.Hr(),
    html.Div(id='top-opportunity-output')
])

# Step 6: Display Sorted Data
@app.callback(
    Output("crypto-arbitrage-graph", "figure"), 
    Input("crypto-arbitrage-graph", "clickData")
)
def display_sorted_data(clickData):
    scale = 'viridis'  # Set a fixed color scale
    fig = px.bar(sorted_df, x="Cryptocurrency", y="Arbitrage_Opportunity", color="Arbitrage_Opportunity", color_continuous_scale=scale)
    fig.update_layout(title="Sorted Cryptocurrency Arbitrage Opportunities", xaxis_title="Cryptocurrency", yaxis_title="Arbitrage Opportunity")
    return fig

# Step 7: Print Top Opportunity
@app.callback(
    Output("top-opportunity-output", "children"), 
    Input("crypto-arbitrage-graph", "clickData")
)
def print_top_opportunity(clickData):
    if clickData:
        crypto_name = clickData['points'][0]['x']
        opportunity = sorted_df.loc[sorted_df["Cryptocurrency"] == crypto_name, "Arbitrage_Opportunity"].values[0]
        return f"Your oppurtunity cost {crypto_name} is {opportunity}"
    return ""

# Step 8: Run the Dash app
if __name__ == "__main__":
    app.run_server(debug=True)
    
def get_kucoin_prices():
    url = 'https://api.kucoin.com/api/v1/market/orderbook/level1'
    params = {
        'symbol': 'BTC-USDT,ETH-USDT,XRP-USDT,LTC-USDT,BCH-USDT,EOS-USDT,XLM-USDT,TRX-USDT,ADA-USDT,XMR-USDT'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = {item['symbol']: float(item['bestAsk']) for item in data['data']}
        return prices
    else:
        print('Failed to fetch data from KuCoin API')
        return None

def get_zebpay_prices():
    url = 'https://www.zebapi.com/pro/v1/market'
    params = {'currencyCode': 'INR'}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        prices = {item['symbol']: float(item['last']) for item in data}
        return prices
    else:
        print('Failed to fetch data from ZebPay API')
        return None

if __name__ == "__main__":
    kucoin_prices = get_kucoin_prices()
    zebpay_prices = get_zebpay_prices()
    
    if kucoin_prices:
        print("KuCoin Prices:")
        for symbol, price in kucoin_prices.items():
            print(f"{symbol}: {price}")
    
    if zebpay_prices:
        print("\nZebPay Prices:")
        for symbol, price in zebpay_prices.items():
            print(f"{symbol}: {price}")
