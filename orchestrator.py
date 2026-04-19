# from langgraph.graph import StateGraph, END
# from agents.retrieval_planner_agent import retrieval_planner_agent
# from agents.product_agent import product_agent
# from agents.order_agent import order_agent

# def build_graph():

#     workflow = StateGraph(dict)

#     # Nodes (Agents)
#     workflow.add_node("retrieval_planner", retrieval_planner_agent)
#     workflow.add_node("product_agent", product_agent)
#     workflow.add_node("order_agent", order_agent)

#     # Flow
#     workflow.set_entry_point("retrieval_planner")
#     workflow.add_edge("retrieval_planner", "product_agent")
#     workflow.add_edge("product_agent", "order_agent")
#     workflow.add_edge("order_agent", END)

#     return workflow.compile()


from langgraph.graph import StateGraph, END
from agents.retrieval_planner_agent import retrieval_planner_agent
from agents.product_agent import product_agent
from agents.order_agent import order_agent


def should_plan(state):
    return "planner_output" not in state

def should_fetch_products(state):
    return "filtered_products" not in state and "planner_output" in state

def should_order(state):
    return "order_text" in state and "order_status" not in state


builder = StateGraph(dict)

builder.add_node("planner", retrieval_planner_agent)
builder.add_node("products", product_agent)
builder.add_node("order", order_agent)


builder.set_entry_point("planner")

builder.add_conditional_edges(
    "planner",
    lambda s: "products" if should_fetch_products(s) else END
)

builder.add_conditional_edges(
    "products",
    lambda s: "order" if should_order(s) else END
)
# builder.add_edge("products", "order")

builder.add_conditional_edges(
    "order",
    lambda s: END
)

graph = builder.compile()