from agents.order_agent import parse_order_with_llm
from tests.schemas import OrderItem

def test_order_parsing_semantic_correctness():

    products = [
        {"id": 1, "title": "Tea Biscuits", "price": 5.0},
        {"id": 2, "title": "Chocolate Cookies", "price": 6.0},
        {"id": 3, "title": "Potato Chips", "price": 4.0},
    ]

    user_input = "I want 2 packs of the biscuits and one chips"

    result = parse_order_with_llm(user_input, products)

    # schema check
    for item in result:
        OrderItem(**item)

    # semantic expectation
    ids = [i["id"] for i in result]
    assert 1 in ids
    assert 3 in ids