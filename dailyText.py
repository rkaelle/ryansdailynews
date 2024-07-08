from twilio.rest import Client
import os

def send_daily_sms():
    account_sid = os.environ['TWILIO_SID']
    auth_token = os.environ['TWILIO_TOKEN']
    client = Client(account_sid, auth_token)
    my_number = os.getenv('MY_NUMBER')

    try:
        message = client.messages.create(
            body = ("What skill are you learning today?\n"
                    "Skill you are learning right now?\n"
                    "Reflection on the day yesterday\n"
                    "Favorite food yesterday\n"
                    "Respond By 6AM"
                    ),
            from_='+18449035435', 
            to='+19258859358'
        )
        print(f"Message sent: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {e}")

if __name__ == "__main__":
    send_daily_sms()