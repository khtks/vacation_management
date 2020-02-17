from application import db, api
from application.models.user import User
from application.schemata.user import UserSchema
from flask import Blueprint, request, Response
from flask_restful import Resource

user_bp = Blueprint("users", __name__, url_prefix='/users')
user_schema = UserSchema()
session = db.session
api = api(user_bp)


class AllUsers(Resource):
    def get(self):
        user = User.query.get(request.form.get('id'))

        if not user.admin:
            return Response(user_schema.dumps(user), 401, mimetype='application/json')
        result = User.query.all()
        return Response(user_schema.dumps(result, many=True), 200, mimetype='application/json')

    def post(self):
        user = user_schema.load(request.form)
        db.session.add(user)
        db.session.commit()
        return Response(user_schema.dumps(user), 201, mimetype='application/json')


class SpecificUser(Resource):
    def get(self, id):
        data = request.form
        target_user = User.query.get(id)
        request_user = User.query.get(data.get('id'))

        if not request_user.admin and data.get('id') != str(id):
            return Response(user_schema.dumps(request_user), 401, mimetype='application/json')
        if not target_user:
            return Response(user_schema.dumps(target_user), 400, mimetype='application/json')

        return Response(user_schema.dumps(target_user), 200, mimetype='application/json')

    def put(self, id):
        data = request.form
        target_user = User.query.get(id)
        request_user = User.query.get(data['id'])

        if request_user.admin: # 사용자가 관리자일 경우
            if target_user.admin and request_user.id != target_user.id: # 수정하려고 하는 대상이 관리자이고 자기 자신이 아닌 경우
                return Response(user_schema.dumps(target_user), 400, mimetype='application/json')
            else: # 수정하려고 하는 대상이 일반 사용자이거나, 자기 자신일 경우
                if data.get('google_id'):
                    target_user.google_id = data['google_id']
                if data.get('ko_name'):
                    target_user.ko_name = data['ko_name']
                if data.get('en_name'):
                    target_user.en_name = data['en_name']
                if data.get('entry_date'):
                    target_user.entry_date = data['entry_date']
                if data.get('admin'):
                    target_user.admin = data['admin']

        else: # 사용자가 일반 사용자일 경우
            if id != int(data['id']): # 수정하려고 하는 대상이 자기 자신이 아닌 경우
                return Response(user_schema.dumps(target_user), 400, mimetype='application/json')
            elif id == int(data['id']): # 수정하교 하는 대상이 자기 자신일 경우
                if data.get('google_id'):
                    target_user.google_id = data['google_id']
                if data.get('en_name'):
                    target_user.en_name = data['en_name']
                if data.get('ko_name'):
                    target_user.ko_name = data['ko_name']
                if data.get('entry_date'):
                    target_user.entry_date = data['entry_date']
                if data.get('admin'): # 일반 사용자는 admin 수정 불가
                    return Response(user_schema.dumps(target_user), 401, mimetype='application/json')

        session.commit()
        return Response(user_schema.dumps(target_user), 200, mimetype='application/json')

    def delete(self, id):
        request_user = User.query.get(request.form['id'])

        if not request_user.admin:
            return Response(user_schema.dumps(request_user), 401, mimetype='application/json')

        target_user = User.query.get(id)
        if not target_user or target_user.admin:  # 삭제하려는 대상이 존재하지 않는 경우
            return Response(user_schema.dumps(target_user), 400, mimetype='application/json')

        db.session.delete(target_user)
        db.session.commit()
        return Response(user_schema.dumps(request_user), 200, mimetype='application/json')


api.add_resource(AllUsers, '/')
api.add_resource(SpecificUser, '/<int:id>')
