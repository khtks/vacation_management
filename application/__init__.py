from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

from application.config import DevelopmentConfig

db = SQLAlchemy()


def create_app(test_config=None):
    # create and configure the application

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig())

    db.init_app(app)

    from application.db_test import test
    app.register_blueprint(test.db_test_bp)

    @app.route('/')
    def init():
        return "init", 200

    @app.route('/hello')
    def hello():
        return "hello", 200

    return app
