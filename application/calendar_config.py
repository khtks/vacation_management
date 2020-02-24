from __future__ import print_function

import os
import pickle

from google_auth_httplib2 import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from application.views.google_api import credentials_to_dict
from googleapiclient.discovery import build
import google.oauth2.credentials
import datetime
from flask import session, redirect


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
                'C:\\Users\\khtks\\PycharmProjects\\vacation_management\\application\\oauth_cred.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    maxResult = 2500
    return service
