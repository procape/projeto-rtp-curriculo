import os
import secrets
import smtplib
from email.mime.text import MIMEText


def create_token():
    return secrets.token_urlsafe(6)


def send_email(recipient, token):
    sender = os.getenv("EMAIL_SENDER")
    password = os.getenv("EMAIL_PASSWORD")

    message = MIMEText(f"Seu token de recuperação de senha é: {token}")
    message["Subject"] = "Recuperação de Senha"
    message["From"] = sender
    message["To"] = recipient

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.send_message(message)
    server.quit()
