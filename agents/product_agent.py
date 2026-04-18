from langchain_community.llms import Ollama
# from tools.product_api_tool import fetch_products
from tools.product_api_tool import (
    fetch_products,
    get_categories,
    execute_retrieval_plan,
    build_product_embeddings,
    semantic_search,
)
from logger.logger import log
import json

llm = Ollama(model="llama3:8b")

def product_agent(state):

    query = state["user_query"]

    print("Finding best products for your preferences...")

    available_categories = get_categories();

    # product retrivel planner LLM prompt to decide the best retrieval strategy (search, category, or general) and the relevant search term or category for the user query. The LLM will return a retrieval plan in a specific JSON format that indicates which strategy to use, what value to search for, and how many pages of results to retrieve.
    prompt = f"""
        You are a product retrieval planner.

        User query: {query}
        Available categories: {available_categories}

        You can request from:
        - https://dummyjson.com/products/search?q=…
        - https://dummyjson.com/products/category-list
        - https://dummyjson.com/products/category/{{category}}

        Your have to do the followings:
        1. make a GET request https://dummyjson.com/products/category-list and explore the category list, Otherwise refer the provided available categories list. You MUST use the category list to inform your decision. Do NOT ignore the category list.
        2. Understand the user query meaning wisely. Then try to match the user query with one of the categories from the list. If there is a good match, choose that category for retrieval. If not, choose search strategy with a good search term.
        3. Analyze the user query and decide whether one of the categories from the list is a good fit for retrieval. If yes, choose category from the list. If not, choose search strategy with a good search term.
        4. If you are selecting category, make sure to choose the most relevant category from the category list. If you are selecting search strategy, make sure to choose a good search term that can retrieve relevant products.
        5. Do not choose a category that is not in the category list. If you are selecting a category, it must be from the category list. Do not choose search strategy if the user query can be well matched with a category from the category list.
        6. If you are select to search using search strategy, make sure to choose a good search term that can retrieve relevant products. The search term should be concise and directly related to the user query. But search term should not be too long. It should be a few words that capture the essence of the user query. So the search term cannot be the same as the user query. It should be a concise term that can retrieve relevant products.
        7. Decide how many pages to retrieve (each page has 30 products). If the user query is very specific, 1 page is enough. If the user query is more general, you can choose to retrieve more pages (up to 5).
        8. ONLY return a valid JSON with:
        - strategy: "search" or "category" or "general"
        - value: text for search or category name
        - pages: number of pages to fetch

        Return ONLY valid JSON with:
        - strategy: "search" or "category" or "general"
        - value: text for search or category name
        - pages: number of pages to fetch
        {"{"}"strategy":"", "value":"", "pages":1{"}"}

        DO NOT write any code. DO NOT explain anything. DO NOT return any text other than the required JSON.
    """
    resp = llm.invoke(prompt)

    log("product retrivel planner LLM response")
    log(resp)

    try:
        plan = json.loads(resp)
    except:
        plan = {"strategy": "search", "value": query, "pages": 1}

    # Executing the retrieval plan according to the LLM's decision specfication and fetchin the relavnt products
    products = execute_retrieval_plan(plan)

    '''
    # print("products")
    # print(products)
    # products = fetch_products()
    '''

    # embedding the products and the user query, then doing semantic search to find the most relevant products to the user query
    embeddings = build_product_embeddings(products)
    candidates = semantic_search(query, products, embeddings)

    # sending the candidates to another LLM to select the best 3 products for the user based on the semantic search results
    prompt = f"""
        You are an intelligent shopping assistant.

        User request: {query}

        Here are the most semantically relevant products:
        {candidates}

        Select the BEST 3-6 for the user.

        Instructions:
        - Do NOT write any code
        - Do NOT explain anything
        - ONLY return a valid JSON array
        - Select the best 3 - 6 matching products
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

    response = llm.invoke(prompt)

    log("Best relavance products LLM response")
    log(response)

    state["filtered_products"] = response
    return state