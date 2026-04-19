import smtplib
from email.mime.text import MIMEText
from logger.logger import log
from typing import Dict

def send_email(to_email: str, content: str) -> None:
    """
    Send a confirmation email to the specified recipient.

    Args:
        to_email (str): Recipient's email address.
        content (str): Content of the email.
    """
    log("tool invoking - Sending confirmation mail")

    sender = "cmal553@gmail.com"
    password = "zvlymgydojaiklyh"

    body = generate_order_email_body(content)
    print("\nOrder Placed Successfully!\n")
    print(body)

    msg = MIMEText(body)
    msg["Subject"] = "Order Confirmation"
    msg["From"] = sender
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.sendmail(sender, to_email, msg.as_string())
    server.quit()

def generate_order_email_body(order: Dict) -> str:
    """
    Generate the body of the order confirmation email.

    Args:
        order (Dict): Dictionary containing order details.

    Returns:
        str: Formatted email body.
    """
    products = order.get("product", [])
    email = order.get("email", "N/A")
    timestamp = order.get("timestamp", "N/A")

    body = []
    body.append("ORDER CONFIRMATION\n")
    body.append(f"Email: {email}")
    body.append(f"Order Time: {timestamp}\n")

    body.append("Ordered Products:\n")

    total = 0

    for idx, p in enumerate(products, start=1):
        title = p.get("title", "N/A")
        price = p.get("price", 0)
        quantity = p.get("quantity", 0)
        pid = p.get("id", "N/A")

        total += price * quantity

        body.append(f"{idx}. {title}")
        body.append(f"   Product ID: {pid}")
        body.append(f"   Price: ${price:.2f}\n")
        body.append(f"   ${price:.2f} * {quantity} = ${price * quantity:.2f}\n")

    body.append("━━━━━━━━━━━━━━━━━━━━")
    body.append(f"TOTAL: ${total:.2f}")
    body.append("━━━━━━━━━━━━━━━━━━━━\n")

    body.append("Thank you for your order!")
    body.append("Your items will be processed shortly.\n\n")

    return "\n".join(body)