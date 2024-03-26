import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random

# Sample DataFrame (replace this with your actual data)
crypto_data_df = pd.DataFrame({
    'Day': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    'Exchange_A': [random.uniform(40000, 45000) for _ in range(5)],
    'Exchange_B': [random.uniform(39000, 46000) for _ in range(5)],
    'Exchange_C': [random.uniform(38000, 47000) for _ in range(5)],
    # Add more exchanges as needed
})

# BST Node class
class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key

# BST class
class BST:
    def __init__(self):
        self.root = None

    # Insertion method
    def insert(self, root, key):
        if root is None:
            return Node(key)
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)
        return root

    # Inorder traversal (sorted order)
    def inorder_traversal(self, root, sorted_data):
        if root:
            self.inorder_traversal(root.left, sorted_data)
            sorted_data.append(root.key)
            self.inorder_traversal(root.right, sorted_data)
        return sorted_data

# Create a BST and insert the data into it
bst = BST()
for exchange in crypto_data_df.columns[1:]:
    for price in crypto_data_df[exchange]:
        bst.root = bst.insert(bst.root, price)

# Define sorting options
sorting_options = ['Day'] + list(crypto_data_df.columns[1:])

# Sort the data based on the selected column
def sort_data(sort_by):
    if sort_by == 'Day':
        sorted_data_df = crypto_data_df.copy()
    else:
        sorted_data = bst.inorder_traversal(bst.root, [])
        sorted_data_df = pd.DataFrame({'Price': sorted_data})
        sorted_data_df['Day'] = crypto_data_df['Day']
        sorted_data_df = sorted_data_df.sort_values(by=[sort_by])
    return sorted_data_df

# Plot the bar chart
def plot_bar_chart(sort_by):
    sorted_data_df = sort_data(sort_by)
    plt.bar(sorted_data_df['Day'], sorted_data_df[sort_by])
    plt.xlabel('Day of the Week')
    plt.ylabel('Price')
    plt.title(f'Cryptocurrency Prices Across Exchanges (Sorted by {sort_by})')
    plt.show()

# Run the function to plot the bar chart
plot_bar_chart('Day')  # Default sorting by Day
