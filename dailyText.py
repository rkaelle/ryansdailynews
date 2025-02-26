from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_daily_sms():
    account_sid = os.environ['TWILIO_SID']
    auth_token = os.environ['TWILIO_TOKEN']
    client = Client(account_sid, auth_token)

    try:
        message = client.messages.create(
            body = ("What skill are you learning today?\n"
                    "Write a brief reflection on the day yesterday?\n"
                    "What was your favorite food you ate yesterday?\n"
                    "~Respond By 6AM~"
                    ),
            from_='+18553942449', 
            to='+19258859358'
        )
        print(f"Message sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")

if __name__ == "__main__":
    send_daily_sms()