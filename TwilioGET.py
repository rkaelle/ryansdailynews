from twilio.rest import Client
import os

# Your Account SID and Auth Token from twilio.com/console
account_sid = os.environ['TWILIO_SID']
auth_token = os.environ['TWILIO_TOKEN']
client = Client(account_sid, auth_token)

# Fetching messages and sorting by date received descending to get the most recent one
def get_most_recent_message():
    messages = client.messages.list(limit=20)  # Fetches last 20 messages; adjust as needed
    return (messages[0] if messages else None)

