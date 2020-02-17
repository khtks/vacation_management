from application import db
from application.models.used_vacation import UsedVacation
from flask import Blueprint

used_vacation_bp = Blueprint("used_vacation", __name__, url_prefix='/users/vacations/used')
