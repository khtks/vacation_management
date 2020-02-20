from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import datetime


def get_service():

    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None

    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Users\\khtks\\PycharmProjects\\vacation_management\\application\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    maxResult = 2500
    return service


def get_events(service):
    events = service.events().list(
        calendarId='primary', timeMin=datetime.datetime(2020, 1, 1).isoformat() + 'Z', showDeleted=True,
        timeMax=datetime.datetime(2020, 2, 28).isoformat() + 'Z', maxResults=2500, singleEvents=True,
        orderBy='startTime'
    ).execute().get('items', [])
    return events