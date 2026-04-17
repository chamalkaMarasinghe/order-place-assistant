import json
from datetime import datetime

def save_order(order: dict):
    """Save order to orders.json"""
    order["timestamp"] = str(datetime.now())

    try:
        with open("orders.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(order)

    with open("orders.json", "w") as f:
        json.dump(data, f, indent=2)