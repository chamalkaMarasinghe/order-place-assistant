import json
import os

def evaluate():
    assert os.path.exists("orders.json"), "orders.json not found"

    with open("orders.json") as f:
        data = json.load(f)

    assert len(data) > 0, "No orders saved"

    print("Evaluation Passed")

if __name__ == "__main__":
    evaluate()