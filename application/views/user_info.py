from application import db, api
from application.models.user_info import UserInfo
from application.schemata.user_info import UserInfoSchema
from flask import Blueprint, request, make_response, jsonify
from flask_restful import Resource

user_info_bp = Blueprint("user_info", __name__, url_prefix='/user-info')
info_schema = UserInfoSchema()
session = db.session
user_schema = UserInfoSchema()

api = api(user_info_bp)


class AllUsers(Resource):
    def get(self):
        result = UserInfo.query.all()
        return make_response(user_schema.dumps(result, many=True), 200)

    def post(self):
        user = UserInfo(google_id=request.form['google_id'], en_name=request.form['en_name'])
        session.add(user)
        session.commit()
        return make_response(user_schema.dumps(user), 201)

    def delete(self):
        session.query(UserInfo).delete()
        session.commit()
        result = session.query(UserInfo).all()
        return make_response(user_schema.dumps(result), 200)


class User(Resource):
    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


api.add_resource(AllUsers, '/', methods=['GET', 'POST', 'DELETE'])
api.add_resource(User, '/<string:google_id>', methods=['GET', 'PUT', 'DELETE'])
