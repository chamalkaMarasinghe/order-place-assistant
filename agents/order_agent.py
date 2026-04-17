from langchain_community.llms import Ollama
from tools.file_tool import save_order
from tools.email_tool import send_email
import json

llm = Ollama(model="llama3:8b")

def order_agent(state):

    products = state["filtered_products"]

    products = print_products(products)

    confirm = input("\nDo you want to place the order? (yes/no): ")

    if confirm.lower() == "yes":

        # natural language order input
        user_order_text = input("\nDescribe your order : ")

        structured_order = parse_order_with_llm(user_order_text, products)

        if not structured_order:
            print("Could not understand order. Please try again.")
            state["order_status"] = "failed"
            return state

        email = input("Enter your email: ")

        order = {
            "product": structured_order,
            "email": email
        }

        save_order(order)
        send_email(email, order)

        state["order_status"] = "confirmed"
    else:
        state["order_status"] = "cancelled"

    return state

def parse_order_with_llm(user_input, products):
    prompt = f"""
        You are an order extraction system.

        User ordered items in natural language:
        "{user_input}"

        Here is the available product list:
        {products}

        Your job:
        - Identify which products the user is referring to (by id or title similarity)
        - Extract quantity for each item (default = 1 if not mentioned)
        - Match products intelligently using meaning, not exact text

        Instructions:
        - Do NOT write any code
        - Do NOT explain anything
        - ONLY return a valid JSON array
        - Each item must contain: id, title, price, quantity

        STRICT OUTPUT RULES:
        - Return ONLY valid JSON array
        - No explanation
        - No text before or after JSON

        Required JSON format::
        [
            {{"id": number, "title": string, "price": number, "quantity": number}}
        ]
    """

    response = llm.invoke(prompt)

    try:
        return json.loads(response)
    except:
        return []

def print_products(products_raw):

    # print(products_raw)

    # If LLM returned a string, convert it to Python list
    if isinstance(products_raw, str):
        products_list = json.loads(products_raw)
    else:
        products_list = products_raw

    print("\nTop Recommended Products:\n")
    
    for index, product in enumerate(products_list, start=1):
        title = product.get("title", "N/A").strip()
        price = product.get("price", "N/A")
        pid = product.get("id", "N/A")

        print(f"{index}. {title}")
        print(f"   Price: ${price:.2f}" if isinstance(price, (int, float)) else f"   Price: {price}")
        print(f"   Product ID: {pid}\n")
    
    return products_list