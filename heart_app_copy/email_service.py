import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()

# Define the send_mail function
def send_mail(to_email, subject, body):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv("EMAIL_ADDRESS")  # Replace with your Gmail address
    sender_password = os.getenv("EMAIL_PASSWORD")  # Replace with your Gmail App Password

    try:
        # Create the email content
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = sender_email
        message["To"] = to_email

        # Connect to the Gmail SMTP server
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Start TLS encryption
            server.login(sender_email, sender_password)  # Log in to the SMTP server
            server.send_message(message)  # Send the email

        return True  # Email sent successfully
    except Exception as e:
        print("Error sending email:", e)
        return False  # Email sending failed
