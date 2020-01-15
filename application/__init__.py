from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(mode='test'):
    # create and configure the application

    app = Flask(__name__)

    from application.config import config_name
    app.config.from_object(config_name[mode])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)

    from application.views import post
    app.register_blueprint(post.post_bp)

    @app.route('/')
    def init():
        return render_template('homepage.html')

    return app
