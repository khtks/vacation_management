from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow, pprint
from flask_migrate import Migrate
from flask_restful import Api


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
api = Api


def create_app(mode='test'):
    # create and configure the application

    app = Flask(__name__)

    from application.config import config_name
    app.config.from_object(config_name[mode])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from application.views.user_info import user_info_bp
    from application.views.used_vacation import used_vacation_bp
    from application.views.remain_vacation import remain_vacation_bp
    app.register_blueprint(user_info_bp)
    app.register_blueprint(used_vacation_bp)
    app.register_blueprint(remain_vacation_bp)

    @app.route('/')
    def init():
        return "Vacation Management Project"

    return app
