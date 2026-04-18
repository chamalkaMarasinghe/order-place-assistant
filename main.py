from langgraph.graph import StateGraph
from agents.product_agent import product_agent
from agents.order_agent import order_agent
from logger.logger import log

def run():
    user_query = input("\n\nWhat product do you want? ")

    state = {
        "user_query": user_query,
        "filtered_products": None,
        "order_status": None
    }

    log("Starting Product Agent")
    state = product_agent(state)

    log("Starting Order Agent")
    state = order_agent(state)

    log(f"Finished with status: {state['order_status']}")

if __name__ == "__main__":
    run()