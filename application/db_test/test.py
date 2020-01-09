from flask import Flask, request, render_template, Blueprint
from application import model

db_test_bp = Blueprint("db_test", __name__, url_prefix='/db', template_folder='templates')

@db_test_bp.route('/main')
def main():
    return render_template('main.html')

@db_test_bp.route('/create')
def create():
    with Flask.app_context():
        model.db.create_all()
    return 'End create'
