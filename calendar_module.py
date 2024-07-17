from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os
from zoneinfo import ZoneInfo  # Python 3.9 and later

def fetch_events():
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    redirect_uri_port = 57874  # Define a fixed port for the redirect URI

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes=scopes)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None  # Invalidate the creds if refresh fails
        if not creds:  # If creds are still not valid, reauthenticate
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, scopes=scopes)
            # Specify the fixed port for redirect URI
            creds = flow.run_local_server(port=redirect_uri_port)
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    # Adjust for PST Timezone
    tz = ZoneInfo("America/Los_Angeles")
    now = datetime.datetime.now(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now + datetime.timedelta(days=1)

    calendar_id = '844fd63e49f5bda51201633b90c3d09e93d27b43ff644f85ca9dcba5b3ab1fd7@group.calendar.google.com'
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now.isoformat(),
        timeMax=end_of_day.isoformat(),
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    # Format event list to show only time in PST with HTML formatting
    formatted_events = []
    for event in events:
        start_time = datetime.datetime.fromisoformat(event['start'].get('dateTime')).astimezone(tz).strftime('%I:%M%p').lower().lstrip('0')
        end_time = datetime.datetime.fromisoformat(event['end'].get('dateTime')).astimezone(tz).strftime('%I:%M%p').lower().lstrip('0')
        event_html = f"<span class='highlight'>{event['summary']}</span>: <span class='time'>{start_time} – {end_time}</span>"
        formatted_events.append(event_html)

    return formatted_events