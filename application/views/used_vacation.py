from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from application import db, api
from application.models.used_vacation import UsedVacation
from flask import Blueprint, Response
from flask_restful import Resource

used_vacation_bp = Blueprint("used_vacation", __name__, url_prefix='/users/vacations/')
api = api(used_vacation_bp)

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


class UserUsedVacation(Resource):
    def get(self, id):
        pass

    def post(self, id):
        events_result = service.events().list(
            calendarId='bluewhale.kr_0gbuu26gl7vue837u7f07mn360@group.calendar.google.com', timeMin=datetime.datetime(2019, 1, 1).isoformat() + 'Z',
            timeMax=datetime.datetime(2020, 2, 28).isoformat() + 'Z', maxResults=maxResult, singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        for event in events:
            summary = event['summary']
            google_id = event['creator'].get('email')
            start = event['start'].get('date') if event['start'].get('date') else event['start'].get('dateTime')[0:10]
            end = event['end'].get('date') if event['end'].get('date') else event['end'].get('dateTime')[0:10]
            event_id = event['id']
            used_vacation = None

            if "휴가" in summary and "대체" not in summary and "반차" not in summary:
                used_vacation = UsedVacation(google_id=google_id, start_date=start, end_date=end, type="vacation", event_id=event_id)
            if "연차" in summary and "대체" not in summary and "반차" not in summary:
                used_vacation = UsedVacation(google_id=google_id, start_date=start, end_date=end, type="vacation", event_id=event_id)
            if "반차" in summary:
                used_vacation = UsedVacation(google_id=google_id, start_date=start, end_date=end, type="half", event_id=event_id)

            if not UsedVacation.query.filter_by(event_id = event_id).first() and used_vacation is not None:
                db.session.add(used_vacation)
                db.session.commit()

        return Response("register used vacation", 200)


api.add_resource(UserUsedVacation, '/used/', '/<string:id>/used/')
