from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Set the Dash app with Bootstrap theme
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

vc_data = {
    "vC": ["BTC", "ETH", "XRP", "LTC", "BCH", "EOS", "XLM", "TRX", "ADA", "XMR", "NEO", "DASH", "ETC", "ZEC", "DOGE", "VET", "BAT", "QTUM", "LSK", "ZRX", "OMG", "NANO", "ICX", "WAVES", "REP", "GNT", "KNC", "CVC", "BNT", "LOOM"],
    "Sambhaavna": [0.05, 0.03, 0.07, 0.02, 0.06, 0.04, 0.08, 0.01, 0.09, 0.05, 0.04, 0.07, 0.03, 0.06, 0.02, 0.08, 0.01, 0.09, 0.05, 0.04, 0.07, 0.03, 0.06, 0.02, 0.08, 0.01, 0.09, 0.05, 0.04, 0.07]
}

df = pd.DataFrame(vc_data)

def merge_sort(arr, key):
    if len(arr) <= 1:
        return
    
    mid = len(arr) // 2
    L = arr[:mid]
    R = arr[mid:]

    merge_sort(L, key)
    merge_sort(R, key)

    i = 0
    j = 0
    k = 0

    while i < len(L) and j < len(R):
        if float(L[i][key]) < float(R[j][key]):
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        k += 1

    while i < len(L):
        arr[k] = L[i]
        i += 1
        k += 1

    while j < len(R):
        arr[k] = R[j]
        j += 1
        k += 1


def merge_sort_dataframe(df, column):
    arr = df.to_dict(orient='records')
    merge_sort(arr, key=column)
    df_sorted = pd.DataFrame(arr)
    return df_sorted

sorted_df = merge_sort_dataframe(df, 'Sambhaavna')

app.layout = html.Div([
    dcc.Graph(id="vc-arbitrage-graph", config={'displayModeBar': False}),
    html.Hr(),
    html.Div(id='top-opportunity-output')
])

@app.callback(
    Output("vc-arbitrage-graph", "figure"),
    Input("vc-arbitrage-graph", "clickData")
)
def display_sorted_data(clickData):
    scale = 'viridis'
    fig = px.bar(sorted_df, x="vC", y="Sambhaavna", color="Sambhaavna", color_continuous_scale=scale)
    fig.update_layout(title="", xaxis_title="VirtualCurrency", yaxis_title="", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font_color="#FFFFFF")
    return fig

@app.callback(
    Output("top-opportunity-output", "children"),
    Input("vc-arbitrage-graph", "clickData")
)
def print_top_opportunity(clickData):
    if clickData:
        vc_name = clickData['points'][0]['x']
        opportunity = sorted_df.loc[sorted_df["vC"] == vc_name, "Sambhaavna"].values[0]
        return f"The top arbitrage opportunity for {vc_name} is {opportunity}"
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)
