from application import db
from application.models.remain_vacation import RemainVacation
from flask import Blueprint

remain_vacation_bp = Blueprint("remain_vacation", __name__, url_prefix='/remain')
