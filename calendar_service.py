from datetime import datetime
import logging
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/calendar']


def authenticate_google_calendar():
    """Authenticate with Google Calendar API and return the service object"""
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('calendar', 'v3', credentials=creds)
    return service


def create_event(calendar_service, summary: str, start_datetime: datetime, end_datetime: datetime, description='', location=''):
    """Create an event in Google Calendar"""
    try:
        event = {
            'summary': summary,
            'description': description,
            'location': location,
            'start': {
                'dateTime': start_datetime.isoformat(),
                'timeZone': 'Europe/Istanbul',
            },
            'end': {
                'dateTime': end_datetime.isoformat(),
                'timeZone': 'Europe/Istanbul',
            },
        }
        event_result = calendar_service.events().insert(calendarId='primary', body=event).execute()
        logging.info(f'Event created: {event_result.get("htmlLink")}')
        print(f'Event created: {event_result.get("htmlLink")}')
        return event_result
    except HttpError as error:
        print(f'An error occurred: {error}')
