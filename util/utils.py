from binance.client import Client
from binance.enums import SIDE_SELL, TIME_IN_FORCE_GTC

def cancel_order(client,symbol, order_id):
    """
    Cancel an order.
    """
    try:
        result = client.cancel_order(symbol=symbol, orderId=order_id)
        print("Order canceled:", result)
    except Exception as e:
        print("Error canceling order:", e)
        
def place_oco_order(client,symbol, quantity, price, stop_price, stop_limit_price):
    """
    Place an OCO (One Cancels the Other) sell order.
    """
    try:
        oco_order = client.create_oco_order(
            symbol=symbol,
            side=SIDE_SELL,
            quantity=quantity,
            price=price,  # Target price
            stopPrice=stop_price,  # Stop price (trigger)
            stopLimitPrice=stop_limit_price,  # Stop-limit price
            stopLimitTimeInForce=TIME_IN_FORCE_GTC
        )
        print("OCO order placed:", oco_order)
        return oco_order
    except Exception as e:
        print("Error placing OCO order:", e)
        return None
    

def get_market_trend(client,symbol, interval='1m', lookback=10):
    """
    Check the market trend based on the moving average of the last 'lookback' candles.
    """
    klines = client.get_klines(symbol=symbol, interval=interval, limit=lookback)
    closes = [float(kline[4]) for kline in klines]
    avg_price = sum(closes) / lookback
    return closes[-1] > avg_price  # Bull market if current price is higher than avg

