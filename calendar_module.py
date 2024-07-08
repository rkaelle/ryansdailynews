from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os
from zoneinfo import ZoneInfo  # Python 3.9 and later

def fetch_events():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes=['https://www.googleapis.com/auth/calendar.readonly'])
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', scopes=['https://www.googleapis.com/auth/calendar.readonly'])
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
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