# main.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
import logging
import time
import datetime
from calendar_module import fetch_events
from responseFormat import process_message_with_openai
#from TwilioGET import get_most_recent_message
from utils import get_current_edition, update_edition_number, ordinal
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
import time

timestamp = int(time.time())


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        #logging.FileHandler("/root/ryansdailynews/main.log"),
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

load_dotenv()

# Firebase initialization
#cred = credentials.Certificate('/root/ryansdailynews/firebaseCredentials.json')
cred = credentials.Certificate('firebaseCredentials.json')
if not firebase_admin._apps:
    initialize_app(cred)
db = firestore.client()

# Email settings
smtp_server = 'smtp.fastmail.com'
port = 587  # starttls
username = os.environ.get('MAIL_USERNAME')
password = os.environ.get('MAIL_PASSWORD')
sender_email = username
ryan_list = ['rkaelle2@gmail.com','rkaelle@umich.edu']

if not username or not password:
    logging.error("Environment variables for MAIL_USERNAME and MAIL_PASSWORD must be set")
    raise ValueError("Environment variables for MAIL_USERNAME and MAIL_PASSWORD must be set")

import imaplib
import email
from email.header import decode_header

def get_most_recent_email_content():
    # IMAP server for Fastmail (adjust if needed)
    imap_server = "imap.fastmail.com"
    username = os.environ.get("MAIL_USERNAME")
    password = os.environ.get("MAIL_READING_PASSWORD")

    # Connect to the IMAP server
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)
    imap.select("INBOX")

    # Search for all emails
    status, messages = imap.search(None, "ALL")
    email_ids = messages[0].split()
    if not email_ids:
        imap.logout()
        return "No emails found."

    # Fetch the most recent email
    latest_email_id = email_ids[-1]
    status, msg_data = imap.fetch(latest_email_id, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    # Extract the email content (plain text preferred)
    email_body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            try:
                part_body = part.get_payload(decode=True).decode()
            except Exception:
                continue
            if content_type == "text/plain" and "attachment" not in content_disposition:
                email_body += part_body
    else:
        email_body = msg.get_payload(decode=True).decode()

    imap.close()
    imap.logout()
    return email_body.strip()

# Read the email HTML template
# with open('/root/ryansdailynews/main.html', 'r') as file:
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
def send_newsletter(db, server, processed_content):
    current_edition_data = get_current_edition(db)
    if not current_edition_data:
        logging.error("Cannot proceed without a current edition.")
        return

    #processed_content = {}
    current_edition_number = get_current_edition(db)

    # skills, reflections, food, science_facts = (
    #     processed_content.get('skills', ''),
    #     processed_content.get('reflections', ''),
    #     processed_content.get('food', ''),
    #     processed_content.get('science', '')
    # )

    skills = processed_content.get('skills', '')
    reflections = processed_content.get('reflections', '')
    food = processed_content.get('food', '')
    science_facts = processed_content.get('science', '')

    # Ensure lists
    if isinstance(skills, str):
        skills = [skills]
    if isinstance(reflections, str):
        reflections = [reflections]
    if isinstance(food, str):
        food = [food]
    if isinstance(science_facts, str):
        science_facts = [science_facts]

    if isinstance(skills, str):
        skills = [skills]
    if isinstance(reflections, str):
        reflections = [reflections]
    if isinstance(food, str):
        food = [food]
    if isinstance(science_facts, str):
        science_facts = [science_facts]

    # Fetch events and other content
    logging.info("Fetching events and content")
    events = fetch_events()

    logging.debug("Fetching users from Firestore")
    users_ref = db.collection('emails')
    users = users_ref.stream()

    users_list = list(users)
    logging.debug(f"Number of users fetched: {len(users_list)}")
    if not users_list:
        logging.error("No users found in the Firestore collection.")
        return

    logging.info("Starting to send emails to users")
    # for index, user in enumerate(users_list):
    #     ensure_smtp_connection(server)  # Ensure connection is still alive
    #     user_data = user.to_dict()
    #     user_name = user_data.get('firstName', 'Valued Member')
    #     user_email = user_data.get('email', sender_email)

    #     logging.info(f"Preparing email for {user_name} ({user_email})")

    #     # HTML content
    #     html_content = base_html_content.replace('{name}', user_name)
    #     html_content = html_content.replace('{edition_number}', ordinal(current_edition_number))
    #     html_content = html_content.replace('{events_list}', f"<ul>{''.join(f'<li>{event}</li>' for event in events)}</ul>")
    #     html_content = html_content.replace('{skills_list}', ''.join(f'{skill}<br>' for skill in skills))
    #     html_content = html_content.replace('{reflections_list}', ''.join(f'{reflection}<br>' for reflection in reflections))
    #     html_content = html_content.replace('{favorite_food}', ''.join(f'{f}<br>' for f in food))
    #     html_content = html_content.replace('{science_facts}', ''.join(f'{fact}<br>' for fact in science_facts))

    #     # Setup the MIME
    #     message = MIMEMultipart()
    #     message['From'] = sender_email
    #     message['To'] = user_email
    #     message['Subject'] = f"Ryan's Daily News {datetime.datetime.now().strftime('%x')}"
    #     message.attach(MIMEText(html_content, 'html'))

    #     # Send the email
    #     try:
    #         server.sendmail(sender_email, user_email, message.as_string())
    #         logging.info(f"Email sent successfully to {user_email}!")
    #     except Exception as e:
    #         logging.error(f"Failed to send email to {user_email}: {e}")

    #     # Delay to avoid hitting the rate limit
    #     if (index + 1) % 7 == 0:
    #         logging.info("Sleeping for 10 minutes to avoid rate limit")
    #         time.sleep(600)  # 10 minutes
    # Define your test email list
    #ryan_list = ['coldclangamingcld@gmail.com', 'isicklgaming@gmail.com']
    ryan_list = ['rkaelle2@gmail.com','rkaelle@umich.edu']

    logging.debug("Starting to send test emails to ryan_list")
    for index, user_email in enumerate(ryan_list):
        ensure_smtp_connection(server)  # Ensure connection is still alive
        user_name = 'Ryan'  # You can set a static name for testing

        logging.debug(f"Preparing email for {user_name} ({user_email})")

        # HTML content
        html_content = base_html_content.replace('{name}', user_name)
        html_content = html_content.replace('{edition_number}', ordinal(current_edition_number))
        html_content = html_content.replace('{events_list}', f"<ul>{''.join(f'<li>{event}</li>' for event in events)}</ul>")
        html_content = html_content.replace('{skills_list}', ''.join(f'{skill}<br>' for skill in skills))
        html_content = html_content.replace('{reflections_list}', ''.join(f'{reflection}<br>' for reflection in reflections))
        html_content = html_content.replace('{favorite_food}', ''.join(f'{f}<br>' for f in food))
        html_content = html_content.replace('{science_facts}', ''.join(f'{fact}<br>' for fact in science_facts))

        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = user_email
        message['Subject'] = f"Ryan's Daily News {datetime.datetime.now().strftime('%x')}"
        message.attach(MIMEText(html_content, 'html'))

        # Send the email
        try:
            server.sendmail(sender_email, user_email, message.as_string())
            logging.info(f"Test email sent successfully to {user_email}!")
        except Exception as e:
            logging.error(f"Failed to send email to {user_email}: {e}")

        # Optional: Add a short delay between emails to mimic real sending behavior
        time.sleep(1)  # Sleep for 1 second

    # Archive the edition and clear current_edition
    send_email_archive_and_clear(db, current_edition_number)

def send_email_archive_and_clear(db, current_edition_number):
    """Archive the current edition and clear the current_edition document."""
    try:
        # Archive the current edition
        editions_ref = db.collection('editions')
        current_edition_ref = db.collection('current_edition').document('current')
        current_edition_doc = current_edition_ref.get()
        if current_edition_doc.exists:
            data = current_edition_doc.to_dict()
            editions_ref.document(str(current_edition_number)).set({
                'content': data.get('content', {}),
                'edition_number': current_edition_number,
                'timestamp': firestore.SERVER_TIMESTAMP
            })
            logging.info(f"Archived edition {current_edition_number}")

        # Increment the edition number
        update_edition_number(db, current_edition_number)

        # Clear the current edition
        current_edition_ref.delete()
        logging.info("Cleared the current edition.")

    except Exception as e:
        logging.error(f"Failed to archive and clear current edition: {e}")

if __name__ == "__main__":

    incoming_email_content = get_most_recent_email_content()
    
    processed_content = process_message_with_openai(incoming_email_content)
    send_newsletter(db, server, processed_content)
    server.quit()
    logging.info("SMTP server connection closed")