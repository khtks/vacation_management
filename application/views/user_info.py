from application import db, api
from application.models.user_info import UserInfo
from application.schemata.user_info import UserInfoSchema
from flask import Blueprint, request, make_response, jsonify, Response
from flask_restful import Resource

user_info_bp = Blueprint("user_info", __name__, url_prefix='/user/info')
user_schema = UserInfoSchema()
session = db.session
api = api(user_info_bp)


class AllUsers(Resource):
    def get(self):
        result = UserInfo.query.all()
        return Response(user_schema.dumps(result, many=True), 200, mimetype='application/json')

    def post(self):
        user = user_schema.load(request.form)
        db.session.add(user)
        db.session.commit()
        return Response(user_schema.dumps(user), 201, mimetype='application/json')


class User(Resource):
    def get(self, id):
        if request.args.get('id') and request.args.get('id') != id:
            user = UserInfo.query.get(request.args.get('id'))
            if user.admin == 0:
                return Response(user_schema.dumps(user), 400, mimetype='application/json')

        result = UserInfo.query.get(id)
        return Response(user_schema.dumps(result), 200, mimetype='application/json')

    def put(self, id):
        data = request.args
        target_user = UserInfo.query.get(id)
        request_user = UserInfo.query.get(data['id'])

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
                if data.get('admin'): # 일반 사용자는 admin 수정 불가
                    return Response(user_schema.dumps(target_user), 401, mimetype='application/json')

        session.commit()
        return Response(user_schema.dumps(target_user), 200, mimetype='application/json')

    def delete(self, id):
        request_user = UserInfo.query.get(request.args['id'])

        if not request_user.admin:
            return Response(user_schema.dumps(request_user), 401, mimetype='application/json')

        target_user = UserInfo.query.get(id)
        if not target_user or target_user.admin:  # 삭제하려는 대상이 존재하지 않는 경우
            return Response(user_schema.dumps(target_user), 400, mimetype='application/json')

        db.session.delete(target_user)
        db.session.commit()
        return Response(user_schema.dumps(request_user), 200, mimetype='application/json')


api.add_resource(AllUsers, '/')
api.add_resource(User, '/<int:id>')
