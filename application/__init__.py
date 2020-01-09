from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


def create_app(mode='prod'):
    # create and configure the application

    app = Flask(__name__)

    from application.config import config_name
    app.config.from_object(config_name[mode])

    from application.model import db
    db.init_app(app)

    @app.route('/')
    def init():
        return "init", 200

    @app.route('/hello')
    def hello():
        return "hello", 200

    return app
