import json
from datetime import datetime
from logger.logger import log
from typing import Dict, List

def save_order(order: Dict) -> None:
    """
    Save an order to the orders.json file.

    Args:
        order (Dict): Dictionary containing order details.
    """
    log("tool invoking - Save order and update orders.json")

    order["timestamp"] = str(datetime.now())

    try:
        with open("orders.json", "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append(order)

    with open("orders.json", "w") as f:
        json.dump(data, f, indent=2)