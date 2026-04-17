from langchain_community.llms import Ollama
from tools.file_tool import save_order
from tools.email_tool import send_email

llm = Ollama(model="llama3:8b")

def order_agent(state):

    products = state["filtered_products"]

    print("\nTop Products:\n", products)

    confirm = input("\nDo you want to place the order? (yes/no): ")

    if confirm.lower() == "yes":
        email = input("Enter your email: ")

        order = {
            "product": products,
            "email": email
        }

        save_order(order)
        send_email(email, "Your order has been placed!")

        state["order_status"] = "confirmed"
    else:
        state["order_status"] = "cancelled"

    return state