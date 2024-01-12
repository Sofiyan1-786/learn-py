import requests
import tkinter as tk

def get_zebpay_xrp_price():
    url = "https://www.zebapi.com/pro/v1/market/XRP-INR/ticker"
    response = requests.get(url)
    data = response.json()
    return float(data['market']) - get_kucoin_xrp_price()

def get_kucoin_xrp_price():
    url = "https://api.kucoin.com/api/v1/market/orderbook/level1?symbol=XRP-USDT"
    response = requests.get(url)
    data = response.json()
    return float(data['data']['price'])

def usd_to_inr(price_usd):
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    inr_rate = data['rates']['INR']
    return price_usd * inr_rate

def calculate():
    input_val = input_entry.get()
    try:
        input_val = float(input_val)
        xrp_zebpay = get_zebpay_xrp_price()
        xrp_kucoin = get_kucoin_xrp_price()
        xrp_kucoin_inr = usd_to_inr(xrp_kucoin)
        
        result_val = (input_val - (input_val * 0.035)) / xrp_kucoin_inr * xrp_zebpay
        output_val = result_val - input_val
        
        result_val_str = "INR {:.2f}".format(result_val)
        output_val_str = "- INR {:.2f}".format(abs(output_val)) if output_val < 0 else "+ INR {:.2f}".format(output_val)
        diff = (xrp_zebpay / xrp_kucoin_inr - 1) * 100
        diff_str = "{:.2f}%".format(diff)
        
        result_label.config(text=result_val_str)
        output_label.config(text=output_val_str)
        diff_label.config(text=diff_str)
    except ValueError:
        result_label.config(text="Invalid input")
        output_label.config(text="")
        diff_label.config(text="")

window = tk.Tk()
window.title("XRP Price Difference Calculator")
window.geometry("400x250")

# Created input label and entry box
input_label = tk.Label(window, text="Enter amount in INR:")
input_label.pack()
input_entry = tk.Entry(window)
input_entry.pack()

# Created calculate button
calculate_button = tk.Button(window, text="Calculate", command=calculate)
calculate_button.pack()

# Created a label for the result
result_label = tk.Label(window, text="")
result_label.pack()

# Created a label for the output
output_label = tk.Label(window, text="")
output_label.pack()

# Created a label for the price difference
diff_label = tk.Label(window, text="")
diff_label.pack()

def refresh():
    calculate()

inr_label1 = tk.Label(window, text="XRP price on Zebpay: INR {:.2f}".format(get_zebpay_xrp_price()))
inr_label1.pack()

inr_label2 = tk.Label(window, text="XRP price on KuCoin: INR {:.2f}".format(get_kucoin_xrp_price()))
inr_label2.pack()

# Run the Tkinter event loop
window.mainloop()
