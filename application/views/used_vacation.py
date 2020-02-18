from application.schemata.used_vacation import UsedVacationSchema
from application.models.used_vacation import UsedVacation
from application.models.user import User
from application.calendar_config import get_service
from application import db, api
from flask import Blueprint, Response, request
from flask_restful import Resource
import datetime


used_vacation_bp = Blueprint("used_vacation", __name__, url_prefix='/users/vacations/')
api = api(used_vacation_bp)
used_vacation_schema = UsedVacationSchema()
maxResult = 2500
service = get_service()
# 'bluewhale.kr_0gbuu26gl7vue837u7f07mn360@group.calendar.google.com'  <== AIMMO Google calednar id


class UserUsedVacation(Resource):
    def get(self, id=None):
        data = request.form

        if User.query.get(data.get('id')).admin == False and id != data.get('id'):
            return Response("No Authority", 401)

        if id is None:
            used_vacation = UsedVacation.query.all()
            return Response(used_vacation_schema.dumps(used_vacation, many=True), 200, mimetype='application/json')

        if id is not None:
            user = User.query.get(id)
            used_vacation = UsedVacation.query.filter_by(user=user).all()
            return Response(used_vacation_schema.dumps(used_vacation, many=True), 200, mimetype='application/json')

    def post(self, id=None):
        events_result = service.events().list(
            calendarId='primary', timeMin=datetime.datetime(2020, 1, 1).isoformat() + 'Z',
            timeMax=datetime.datetime(2020, 2, 28).isoformat() + 'Z', maxResults=maxResult, singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        for event in events:
            user = User.query.filter_by(google_id=event['creator'].get('email')).first()
            start = event['start'].get('date') if event['start'].get('date') else event['start'].get('dateTime')[0:10]
            end = event['end'].get('date') if event['end'].get('date') else event['end'].get('dateTime')[0:10]
            event_id = event['id']
            used_vacation = None

            if "휴가" in event['summary'] and "대체" not in event['summary'] and "반차" not in event['summary']:
                used_vacation = UsedVacation(user=user, start_date=start, end_date=end, type="vacation", event_id=event_id)
            if "연차" in event['summary'] and "대체" not in event['summary'] and "반차" not in event['summary']:
                used_vacation = UsedVacation(user=user, start_date=start, end_date=end, type="vacation", event_id=event_id)
            if "반차" in event['summary']:
                used_vacation = UsedVacation(user=user, start_date=start, end_date=end, type="half", event_id=event_id)

            if used_vacation is not None and not UsedVacation.query.filter_by(event_id=event_id).first():
                db.session.add(used_vacation)
                db.session.commit()

        return Response("register used vacation", 201)

    def delete(self, id=None):
        if id is None:
            events_result = service.events().list(
                calendarId='primary', timeMin=datetime.datetime(2020, 1, 1).isoformat() + 'Z', showDeleted=True,
                timeMax=datetime.datetime(2020, 2, 28).isoformat() + 'Z', maxResults=maxResult, singleEvents=True, orderBy='startTime'
            ).execute()
            events = events_result.get('items', [])

            for event in events:
                if event['status'] == 'cancelled' and UsedVacation.query.filter_by(event_id=event['id']).first():
                    event = UsedVacation.query.filter_by(event_id=event['id']).first()
                    print(event)
                    db.session.delete(event)
                    db.session.commit()

            return Response("used vacation has been deleted", 200)

        if id is not None:
            data = request.form
            print(User.query.get(data.get('id')))
            if not User.query.get(data.get('id')).admin:
                return Response("No Authority", 401)

            user = User.query.get(id)
            events = UsedVacation.query.filter_by(user=user).delete()
            return Response("Delete specific user vacation", 200)


api.add_resource(UserUsedVacation, '/used/', '/<string:id>/used/')
