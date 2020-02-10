from application import db, api
from application.models.user_info import UserInfo
from application.schemata.user_info import UserInfoSchema
from flask import Blueprint, request, make_response, Response
from flask_restful import Resource

user_info_bp = Blueprint("user_info", __name__, url_prefix='/user/info')
user_schema = UserInfoSchema()
session = db.session
api = api(user_info_bp)


class AllUsers(Resource):
    def get(self):
        result = UserInfo.query.all()
        return make_response(user_schema.dumps(result, many=True), 200)

    def post(self):
        user = user_schema.load(request.form)
        db.session.add(user)
        db.session.commit()
        return make_response(user_schema.dumps(user), 201)


class User(Resource):
    def get(self, id):
        if request.args.get('id') and request.args.get('id') != id:
            user = UserInfo.query.get(request.args.get('id'))
            if user.role == 0:
                return make_response(user_schema.dumps(user), 400)

        result = UserInfo.query.get(id)
        return make_response(user_schema.dumps(result), 200)

    def put(self, id):
        pass

    def delete(self, id):
        # if request.args.get('id') and request.args.get('id') != id:
        #     user = UserInfo.query.get(request.args.get('id'))
        #     if user.role == 0:
        #         return make_response(user_schema.dumps(user), 400)
        if request.args.get('id'):
            user = UserInfo.query.get(request.args.get('id'))
            if user.role != 1:
                return make_response(user_schema.dumps(user), 400)

        user = UserInfo.query.get(id)
        user.role = -1
        db.session.commit()
        return make_response(user_schema.dumps(UserInfo.query.get(id)), 200)


api.add_resource(AllUsers, '/')
api.add_resource(User, '/<int:id>')
