from application import db
from application.models.user_info import UserInfo
from flask import Blueprint

user_info_bp = Blueprint("user_info", __name__, url_prefix='/info')
