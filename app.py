import streamlit as st
from langgraph.graph import StateGraph
from agents.product_agent import product_agent
from agents.order_agent import order_agent
from agents.retrieval_planner_agent import retrieval_planner_agent
from logger.logger import log
import json

st.set_page_config(page_title="AI Shopping Assistant", layout="wide")
st.title("🛒 AI Product Recommender")

# -----------------------------
# STEP 1 — Product Search
# -----------------------------
query = st.text_input("What product do you want?")

if st.button("Find Products") and query:

    state = {
        "user_query": query,
        "filtered_products": None,
        "order_status": None
    }

    log("Starting Retrieval Planner Agent")
    state = retrieval_planner_agent(state)

    log("Starting Product Agent")
    log("Finding best products for the query: " + state["user_query"])
    state = product_agent(state)

    # product_agent currently returns JSON string from LLM
    products = json.loads(state["filtered_products"])
    st.session_state["products"] = products
    st.session_state["state"] = state


# -----------------------------
# STEP 2 — Show Products
# -----------------------------
if "products" in st.session_state:

    state = st.session_state["state"]
    st.subheader("Top Recommended Products")

    for p in st.session_state["products"]:
        with st.container(border=True):
            st.write(f"### {p['title']}")
            st.write(f"**Product ID:** {p['id']}")
            st.write(f"**Price:** ${p['price']}")

    # -----------------------------
    # STEP 3 — Order in Plain English
    # -----------------------------
    st.divider()
    st.subheader("Place Your Order")

    order_text = st.text_area(
        "Enter your order in plain English",
    )

    email = st.text_input("Enter your email")

    if st.button("Place Order") and order_text and email:

        state["order_text"] = order_text
        state["email"] = email

        log("Starting Order Agent")
        state = order_agent(state)

        if state["order_status"] == "failed" :
            st.error("Failed to place order. Please try again.")
        else:
            st.success("Order placed and confirmation email sent!")

        log(f"Finished with status: {state['order_status']}")