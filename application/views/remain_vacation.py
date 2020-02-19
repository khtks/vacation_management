from application.schemata.remain_vacation import RemainVacationSchema
from application.models.remain_vacation import RemainVacation
from application.models.user import User
from application import db, api, service
from flask import Blueprint, Response, request
from flask_restful import Resource
import datetime

remain_vacation_bp = Blueprint("remain_vacation", __name__, url_prefix='/users/vacations/')
remain_vacation_schema = RemainVacationSchema()
api = api(remain_vacation_bp)


class UserVacation(Resource):
    def get(self):
        pass

    def post(self):
        pass


api.add_resource(UserVacation, '/remain/', '/<string:id>/remain/')
