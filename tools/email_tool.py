import smtplib
from email.mime.text import MIMEText

def send_email(to_email: str, content: str):
    """Send confirmation email"""
    sender = "cmal553@gmail.com"
    password = "zvlymgydojaiklyh"

    msg = MIMEText(content)
    msg["Subject"] = "Order Confirmation"
    msg["From"] = sender
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender, password)
    server.sendmail(sender, to_email, msg.as_string())
    server.quit()