from flask import Flask


def create_app(mode='test'):
    # create and configure the application

    app = Flask(__name__)

    from application.config import config_name
    app.config.from_object(config_name[mode])

    from application.model import db
    db.init_app(app)

    from application.schema import ma
    ma.init_app(app)

    from application.marshal_test import test
    app.register_blueprint(test.bp)

    @app.route('/')
    def init():
        return "init", 200

    return app
