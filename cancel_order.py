
from app import client

def cancel_order():
    open_orders = client.get_open_orders(symbol='OMUSDT')
    for order in open_orders:
        print(f"Cancelling order: {order['orderId']}")
        client.cancel_order(symbol='OMUSDT', orderId=order['orderId'])

if __name__ == "__main__":
    cancel_order()