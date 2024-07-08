# SMTP and Environment Modules
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Content and Date Modules
import datetime
from calendar_module import fetch_events
from responseFormat import process_message_with_openai
from TwilioGET import get_most_recent_message

# Load environment variables
load_dotenv()

# Firebase initialization
cred = credentials.Certificate('firebaseCredentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


# Email settings
smtp_server = 'smtp.fastmail.com'
port = 587  # starttls
username = os.environ['MAIL_USERNAME']
password = os.environ['MAIL_PASSWORD']
sender_email = username

# Read the email HTML template
with open('main.html', 'r') as file:
    base_html_content = file.read()

# Fetch events and other content
events = fetch_events()
most_recent_message = get_most_recent_message()
processed_content = process_message_with_openai(most_recent_message) if most_recent_message else {}
skills, reflections, science_facts = processed_content.get('skills', []), processed_content.get('reflections', []), processed_content.get('science', [])

# Connect to Fastmail server
server = smtplib.SMTP(smtp_server, port)
server.ehlo()
server.starttls()
server.ehlo()
server.login(username, password)

# Fetch all users from Firestore and send emails
users_ref = db.collection('users')  # Adjust 'users' to your collection name
users = users_ref.stream()

for user in users:
    user_data = user.to_dict()
    user_name = user_data.get('firstName', 'Valued Member')
    user_email = user_data.get('email', sender_email)  # Fallback to sender if no email
    
    # Personalize HTML content
    html_content = base_html_content.replace('{name}', user_name)
    html_content = html_content.replace('{events_list}', ''.join(f"<li>{event}</li>" for event in events))
    html_content = html_content.replace('{skills_list}', ''.join(f"<li>{skill}</li>" for skill in skills))
    html_content = html_content.replace('{reflections_list}', ''.join(f"<li>{reflection}</li>" for reflection in reflections))
    html_content = html_content.replace('{science_facts}', ''.join(f"<li>{fact}</li>" for fact in science_facts))

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = user_email
    message['Subject'] = f"Ryan's Daily News {datetime.datetime.now().strftime('%x')}"
    message.attach(MIMEText(html_content, 'html'))

    # Send the email
    try:
        server.sendmail(sender_email, user_email, message.as_string())
        print(f"Email sent successfully to {user_email}!")
    except Exception as e:
        print(f"Failed to send email to {user_email}: {e}")

# Cleanup
server.quit()