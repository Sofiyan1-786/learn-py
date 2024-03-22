from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Step 1: Fetch Data (Mock Data for demonstration)
crypto_data = {
    "Cryptocurrency": ["BTC", "ETH", "XRP", "LTC", "BCH", "EOS", "XLM", "TRX", "ADA", "XMR"],
    "Arbitrage_Opportunity": [0.05, 0.03, 0.07, 0.02, 0.06, 0.04, 0.08, 0.01, 0.09, 0.05]  # Example arbitrage opportunities
}

df = pd.DataFrame(crypto_data)

# Step 2: Calculate Arbitrage Opportunities

# Step 3: Sort Data
sorted_df = df.sort_values(by="Arbitrage_Opportunity", ascending=False)

# Step 4: Create Dash App
app = Dash(__name__)

colorscales = px.colors.named_colorscales()

app.layout = html.Div([
    html.H4('Cryptocurrency Arbitrage Opportunities'),
    dcc.Dropdown(
        id='colorscales-x-dropdown', 
        options=[{'label': scale, 'value': scale} for scale in colorscales],
        value='viridis'
    ),
    dcc.Graph(id="crypto-arbitrage-graph"),
    html.Hr(),
    html.Div(id='top-opportunity-output')
])

# Step 5: Display Sorted Data
@app.callback(
    Output("crypto-arbitrage-graph", "figure"), 
    Input("colorscales-x-dropdown", "value")
)
def display_sorted_data(scale):
    fig = px.bar(sorted_df, x="Cryptocurrency", y="Arbitrage_Opportunity", color="Arbitrage_Opportunity", color_continuous_scale=scale)
    fig.update_layout(title="Sorted Cryptocurrency Arbitrage Opportunities", xaxis_title="Cryptocurrency", yaxis_title="Arbitrage Opportunity")
    return fig

# Step 6: Print Top Opportunity
@app.callback(
    Output("top-opportunity-output", "children"), 
    Input("crypto-arbitrage-graph", "clickData")
)
def print_top_opportunity(clickData):
    if clickData:
        crypto_name = clickData['points'][0]['x']
        opportunity = sorted_df.loc[sorted_df["Cryptocurrency"] == crypto_name, "Arbitrage_Opportunity"].values[0]
        return f"The top arbitrage opportunity for {crypto_name} is {opportunity}"
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)
