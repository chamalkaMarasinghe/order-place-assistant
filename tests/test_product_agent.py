import json
from agents.product_agent import product_agent
from tests.schemas import Product

def test_product_agent_returns_valid_products():

    state = {
        "user_query": "tea snacks",
        "planner_output": {"strategy": "search", "value": "snacks", "pages": 1}
    }

    state = product_agent(state)

    products = json.loads(state["filtered_products"])

    assert 1 <= len(products) <= 6

    for p in products:
        Product(**p)  # schema validation