from langchain_community.llms import Ollama
# from tools.product_api_tool import fetch_products
from tools.product_api_tool import (
    fetch_products,
    build_product_embeddings,
    semantic_search,
)
import json

llm = Ollama(model="llama3:8b")

def product_agent(state):

    query = state["user_query"]

    print("Finding best products for your preferences...")

    products = fetch_products()
    embeddings = build_product_embeddings(products)
    candidates = semantic_search(query, products, embeddings)

    prompt = f"""
        You are an intelligent shopping assistant.

        User request: {query}

        Here are the most semantically relevant products:
        {candidates}

        Select the BEST 3 for the user.

        Instructions:
        - Do NOT write any code
        - Do NOT explain anything
        - ONLY return a valid JSON array
        - Select the best 3 matching products
        - Each item must contain: id, title, price

        Return format example:
        [
        {{"id": 1, "title": "Product name", "price": 10.5}}
        ]
        """

    response = llm.invoke(prompt)

    state["filtered_products"] = response
    return state