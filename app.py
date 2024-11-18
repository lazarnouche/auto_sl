import sys
import time
from binance.client import Client
from binance.enums import *
import pandas as pd
import sys
sys.path.insert(0, '..')
from keys.api_key import BINANCE_KEY_TEST,BINANCE_SECRET_TEST,BINANCE_KEY, BINANCE_SECRET
from util.utils import place_oco_order,cancel_order
import warnings
# Suppress all warnings
warnings.filterwarnings("ignore")
client = None

testnet  = input("Do you wanna use test api ? [yes/no]")

if testnet.lower() == "yes":
    client = Client(BINANCE_KEY_TEST, BINANCE_SECRET_TEST,testnet=True)
    client.API_URL = "https://testnet.binance.vision/api" 
elif testnet.lower() == "no":
    print(""""
    # WARNING: This script interacts with your REAL Binance account. Ensure API keys are secure,
    # test thoroughly on the Binance Testnet, and understand the code before running it live.
          """)
    client = Client(BINANCE_KEY, BINANCE_SECRET)
else:
    raise ValueError("Invalid value provided!")


df = pd.read_csv('setup.csv')
par = df.iloc[0]
crypto = client.get_asset_balance(asset=par.asset)
print(crypto)


def run():

    symbol = par.symbol
    interval = par.interval
    quantity = int(par.quantity)# Adjust quantity based on your balance
    profit_target_percent = par.profit_target_percent  # 2% profit target
    increment_percent = par.increment_percent   # 2% profit target
    stop_loss_percent = par.stop_loss_percent  # 1% stop-loss
    stop_limit_offset_percent = par.stop_limit_offset_percent # Offset for stop-limit price (0.2%)

    oco_order = None  
    # Get the current price
    ticker = client.get_symbol_ticker(symbol=symbol)
    current_price = float(ticker['price'])

    # Calculate target price and stop-loss
    target_price = round(current_price * (1 + profit_target_percent), 2)
    stop_price = round(current_price * (1 - stop_loss_percent), 2)
    stop_limit_price = round(stop_price * (1 - stop_limit_offset_percent), 2)
    increment_price = round(current_price * (1 + increment_percent), 2)

    # Place a new OCO order
    oco_order = place_oco_order(
        client,
        symbol,
        quantity,
        price=str(target_price),
        stop_price=str(stop_price),
        stop_limit_price=str(stop_limit_price)
    )

    if oco_order:
        while True:
            ticker = client.get_symbol_ticker(symbol=symbol)
            new_price = float(ticker['price'])
            print(f"new_price: {new_price},increment_price {increment_price}, stop_price {stop_price}" )
            if new_price > increment_price:
                print("Price increased! Adjusting OCO order...")
                
                # Cancel the current OCO order
                for order in oco_order['orderReports']:
                    cancel_order(client,symbol, order['orderId'])
                
                
                # Update target and stop-loss prices
                target_price = round(new_price * (1 + profit_target_percent), 2)
                stop_price = round(new_price * (1 - stop_loss_percent), 2)
                stop_limit_price = round(stop_price * (1 - stop_limit_offset_percent), 2)
                increment_price = round(new_price * (1 + increment_percent), 2)
                
                # Place a new OCO order
                oco_order = place_oco_order(
                    client,
                    symbol,
                    quantity,
                    price=str(target_price),
                    stop_price=str(stop_price),
                    stop_limit_price=str(stop_limit_price)
                )

            time.sleep(3)  # Adjust the frequency as needed
            if oco_order is None:
                break

if __name__ == "__main__":
    run()


