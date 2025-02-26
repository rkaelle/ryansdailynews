import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

# Email server configuration
smtp_server = 'smtp.fastmail.com'
port = 587  # TLS port
username = os.environ.get('MAIL_USERNAME')
password = os.environ.get('MAIL_PASSWORD')
sender_email = username
recipient_email = 'rkaelle2@gmail.com'

def send_daily_email():
    subject = "(RDN) RESPOND TO THIS"
    body = (
        "What skill are you learning today?\n"
        "Write a brief reflection on the day yesterday?\n"
        "What was your favorite food you ate yesterday?\n"
        "~Respond By 6AM~"
    )

    # Create a MIME multipart message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject

    # Attach the plain text body to the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server and send email
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(username, password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    send_daily_email()