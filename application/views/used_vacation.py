from application.schemata.used_vacation import UsedVacationSchema
from application.models.used_vacation import UsedVacation
from application.models.user import User
from application import db, api
from application.views.google_api import session, get_event
from flask import Blueprint, Response, request, redirect, url_for, make_response, render_template, current_app
from flask_restful import Resource


used_vacation_bp = Blueprint("used_vacation", __name__, url_prefix='/users/vacations/')
used_vacation_schema = UsedVacationSchema()
api = api(used_vacation_bp)
maxResult = 2500
headers = {'Content-Type': 'text/html'}


class UserUsedVacation(Resource):
    def get(self, id=None):
        data = request.args
        request_user = User.query.get(data.get('id'))

        if request_user.admin == False and id != data.get('id'):
            return Response("No Authority", 401)

        if id is None:
            used_vacation = UsedVacation.query.all()
            return make_response(render_template('user/multiple_user_result.html', title="사용한 전체 휴가", result=used_vacation, id=str(request_user.id)), 201, headers)

        if id is not None:
            target_user = User.query.get(id)
            used_vacation = UsedVacation.query.filter_by(user=target_user).all()
            return make_response(render_template('user/multiple_user_result.html', title="사용한 휴가", result=used_vacation, id=str(target_user.id)), 201, headers)

    def post(self, id=None):
        if 'events' not in session:
            events = get_event()
        else:
            events = session['events']

        user = User.query.get(request.form.get('id'))
        result_event = []
        user_id = []

        for event in events:
            if "휴가" in event['summary'] or "연차" in event['summary'] or "반차" in event['summary']:
                if UsedVacation.query.filter_by(event_id=event['id']).one_or_none():
                    continue
                else :
                    user, summary, start, end, type, event_id = Attribute(event)
                    used_vacation = UsedVacation(user=user, summary=summary, start_date=start, end_date=end, type=type, event_id=event_id)

                if used_vacation is not None:
                    if used_vacation.user.id not in user_id:
                        user_id.append(used_vacation.user.id)
                    result_event.append(used_vacation)
                    db.session.add(used_vacation)
                    db.session.commit()

        if not result_event:
            result_event.append("None")

        with current_app.test_client() as client:
            for id in user_id:
                client.put(url_for('remain_vacation.user_vacation'), data=dict(id=id))

        return make_response(render_template('user/multiple_user_result.html', title="등록된 휴가", result=result_event, id=str(user.id), user=user), 201, headers)

    def delete(self, id=None):
        if id is None:
            if 'events' not in session:
                events = get_event()
            else:
                events = session['events']

            for event in events:
                if event['status'] == 'cancelled' and UsedVacation.query.filter_by(event_id=event['id']).first():
                    event = UsedVacation.query.filter_by(event_id=event['id']).first()
                    db.session.delete(event)
                    db.session.commit()
            return True

        if id is not None:
            data = request.form
            if not User.query.get(data.get('id')).admin:
                return Response("No Authority", 401)

            user = User.query.get(id)
            events = UsedVacation.query.filter_by(user=user).delete()
            db.session.commit()
            return Response("Delete specific user vacation", 200)


api.add_resource(UserUsedVacation, '/used', '/<string:id>/used', endpoint='used')


def Attribute(event):
    user = User.query.filter_by(google_id=event['creator'].get('email')).first()
    summary = event['summary']
    start = event['start'].get('date') if event['start'].get('date') else event['start'].get('dateTime')[0:10]
    end = event['end'].get('date') if event['end'].get('date') else event['end'].get('dateTime')[0:10]

    if "휴가" in summary and "대체" not in summary and "반차" not in summary:
        type = "연차"
    if "연차" in summary and "대체" not in summary and "반차" not in summary:
        type = "연차"
    if "반차" in summary:
        type = "반차"

    event_id = event['id']

    return user, summary, start, end, type, event_id
