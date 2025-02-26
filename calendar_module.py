from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os
from zoneinfo import ZoneInfo  # Python 3.9+


def fetch_events():
    creds = None
    token_path = 'token.json'
    credentials_path = 'credentials.json'
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    redirect_uri_port = 57874  # or pick any unused port

    # 1. Load existing user credentials from token.json
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, scopes=scopes)

    # 2. Refresh them if expired, or re-run the Installed App flow if not valid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                creds = None  # If refresh fails, we'll reauthenticate below

        if not creds:
            # 3. Run local server flow to let the user log in
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, scopes=scopes)
            creds = flow.run_local_server(port=redirect_uri_port)

            # 4. Save the credentials for future runs
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

    # 5. Build the Calendar API client
    service = build('calendar', 'v3', credentials=creds)

    # 6. Set times in PST
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

    # 7. Format event list
    formatted_events = []
    for event in events:
        start_time = (datetime.datetime
                      .fromisoformat(event['start'].get('dateTime'))
                      .astimezone(tz)
                      .strftime('%I:%M%p')
                      .lower()
                      .lstrip('0'))
        end_time = (datetime.datetime
                    .fromisoformat(event['end'].get('dateTime'))
                    .astimezone(tz)
                    .strftime('%I:%M%p')
                    .lower()
                    .lstrip('0'))
        event_html = (f"<span class='highlight'>{event['summary']}</span>: "
                      f"<span class='time'>{start_time} – {end_time}</span>")
        formatted_events.append(event_html)

    return formatted_events