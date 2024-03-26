from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import random
crypto_data_df = pd.DataFrame({
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'WazirX': [random.uniform(40000, 45000) for _ in range(5)],
    'Binacne': [random.uniform(39000, 46000) for _ in range(5)],
    'Chutcoin': [random.uniform(38000, 47000) for _ in range(5)],
})

class Node:
    def _init_(self, key):
        self.left = None
        self.right = None
        self.key = key

class BST:
    def _init_(self):
        self.root = None

    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    def inorder_traversal(self, root, sorted_data):
        if root:
            self.inorder_traversal(root.left, sorted_data)
            sorted_data.append(root.key)
            self.inorder_traversal(root.right, sorted_data)
        return sorted_data

bst = BST()
for exchange in crypto_data_df.columns[1:]:
    for price in crypto_data_df[exchange]:
        bst.root = bst.insert(bst.root, price)

sorting_options = ['Day'] + list(crypto_data_df.columns[1:])

def sort_data(sort_by):
    if sort_by == 'Day':
        sorted_data_df = crypto_data_df.copy()
    else:
        sorted_data = bst.inorder_traversal(bst.root, [])
        sorted_data_df = pd.DataFrame({'Price': sorted_data})
        sorted_data_df['Day'] = crypto_data_df['Day']
        sorted_data_df = sorted_data_df.sort_values(by=[sort_by])
    return sorted_data_df

def plot_bar_chart(sort_by):
    sorted_data_df = sort_data(sort_by)
    plt.bar(sorted_data_df['Day'], sorted_data_df[sort_by])
    plt.xlabel('Day of the Week')
    plt.ylabel('Price')
    plt.title(f'Cryptocurrency Prices Across Exchanges (Sorted by {sort_by})')
    plt.show()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(_name_, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Dropdown(
        id='sorting-dropdown',
        options=[{'label': i, 'value': i} for i in sorting_options],
        value='Day'
    ),
    dcc.Graph(id='crypto-bar-chart')
])

@app.callback(
    Output('crypto-bar-chart', 'figure'),
    [Input('sorting-dropdown', 'value')]
)
def update_bar_chart(sort_by):
    sorted_data_df = sort_data(sort_by)
    fig = {
        'data': [{'x': sorted_data_df['Day'], 'y': sorted_data_df[sort_by], 'type': 'bar'}],
        'layout': {
            'xaxis': {'title': 'Day of the Week'},
            'yaxis': {'title': 'Price'},
            'title': f'Cryptocurrency Prices Across Exchanges (Sorted by {sort_by})'
        }
    }
    return fig

