from langchain_community.llms import Ollama
from tools.product_api_tool import (
    get_categories,
    execute_retrieval_plan,
    build_product_embeddings,
    semantic_search,
)
from logger.logger import log
import json

llm = Ollama(model="llama3:8b")

def product_agent(state):
    
    plan = state["planner_output"]
    query = state["user_query"]

    # Executing the retrieval plan according to the LLM's decision specfication and fetchin the relavnt products
    products = execute_retrieval_plan(plan)

    # embedding the products and the user query, then doing semantic search to find the most relevant products to the user query
    embeddings = build_product_embeddings(products)
    candidates = semantic_search(query, products, embeddings)

    # sending the candidates to another LLM to select the best 3 products for the user based on the semantic search results
    system_prompt = f"""
        You are an intelligent shopping assistant.

        User request: {query}

        Here are the most semantically relevant products:
        {candidates}

        Select the BEST 3 to 6 products for the user.

        Instructions:
        - Do NOT write any code
        - Do NOT explain anything
        - ONLY return a valid JSON array
        - Select the best 3 to 6 matching products
        - Each item must contain: id, title, price


        Required JSON format:
        [
            {{"id": number, "title": string, "price": number}}
        ]
        """
        # Return format example:
        # [
        # {{"id": 1, "title": "Product name", "price": 10.5}}
        # ]

    response = llm.invoke(system_prompt)

    log("Best relavance products LLM response")
    log(response)

    state["filtered_products"] = response

    return state