# SMTP and Environment Modules
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
import time

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

# Firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Content and Date Modules
import datetime
from calendar_module import fetch_events
from responseFormat import process_message_with_openai
from TwilioGET import get_most_recent_message
from utils import get_current_edition, update_edition_number, ordinal

# Load environment variables
username = os.environ.get('MAIL_USERNAME')
password = os.environ.get('MAIL_PASSWORD')
if not username or not password:
    logging.error("Environment variables for MAIL_USERNAME and MAIL_PASSWORD must be set")
    raise ValueError("Environment variables for MAIL_USERNAME and MAIL_PASSWORD must be set")

# Firebase initialization
cred = credentials.Certificate('firebaseCredentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

# Email settings
smtp_server = 'smtp.fastmail.com'
port = 587  # starttls
sender_email = username

# Read the email HTML template
with open('main.html', 'r') as file:
    base_html_content = file.read()

# Function to ensure SMTP connection
def ensure_smtp_connection(server):
    try:
        server.noop()  # Test existing connection
    except smtplib.SMTPException as e:
        logging.info("SMTP session expired or failed. Reconnecting...")
        server.connect(smtp_server, port)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(username, password)


# Fetch events and other content
logging.debug("Fetching events and content")
events = fetch_events()
most_recent_message = get_most_recent_message()
current_edition = get_current_edition(db)
processed_content = process_message_with_openai(most_recent_message) if most_recent_message else {}
skills, reflections, science_facts = processed_content.get('skills', []), processed_content.get('reflections', []), processed_content.get('science', [])



# Ensure skills, reflections, and science_facts are lists of strings
if isinstance(skills, str):
    skills = [skills]
if isinstance(reflections, str):
    reflections = [reflections]
if isinstance(science_facts, str):
    science_facts = [science_facts]

# Connect to Fastmail server
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    logging.info("Connected to the SMTP server successfully")
except Exception as e:
    logging.error(f"Failed to connect to the SMTP server: {e}")
    exit(1)

# Fetch all users from Firestore and send emails
logging.debug("Fetching users from Firestore")
users_ref = db.collection('emails')
users = users_ref.stream()

users_list = list(users)
logging.debug(f"Number of users fetched: {len(users_list)}")
if not users_list:
    logging.error("No users found in the Firestore collection.")
    exit(1)

ryan_list = ['rkaelle2@gmail.com','rkaelle@umich.edu']

logging.debug("Starting to send emails to users")
for index, user in enumerate(users_list):
    ensure_smtp_connection(server)  # Ensure connection is still alive
    user_data = user.to_dict()
    user_name = user_data.get('firstName', 'Valued Member')
    user_email = user_data.get('email', sender_email)

    logging.debug(f"Preparing email for {user_name} ({user_email})")

    # HTML content
    html_content = base_html_content.replace('{name}', user_name)
    html_content = html_content.replace('{edition_number}', ordinal(current_edition)) 
    html_content = html_content.replace('{events_list}', f"<ul>{''.join(f'<li>{event}</li>' for event in events)}</ul>")
    html_content = html_content.replace('{skills_list}', f"<ul>{''.join(f'<li>{skill}</li>' for skill in skills)}</ul>")
    html_content = html_content.replace('{reflections_list}', f"<ul>{''.join(f'<li>{reflection}</li>' for reflection in reflections)}</ul>")
    html_content = html_content.replace('{science_facts}', f"<ul>{''.join(f'<li>{fact}</li>' for fact in science_facts)}</ul>")

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = user_email
    message['Subject'] = f"Ryan's Daily News {datetime.datetime.now().strftime('%x')}"
    message.attach(MIMEText(html_content, 'html'))

    # Send the email
    try:
        server.sendmail(sender_email, user_email, message.as_string())
        logging.info(f"Email sent successfully to {user_email}!")
    except Exception as e:
        logging.error(f"Failed to send email to {user_email}: {e}")

    # Delay to avoid hitting the rate limit
    if (index + 1) % 7 == 0:
        logging.debug("Sleeping for 10 minutes to avoid rate limit")
        time.sleep(600)

update_edition_number(db, current_edition)

server.quit()
logging.info("SMTP server connection closed")