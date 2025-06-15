from flask import Flask
from config import config_by_name
from .extensions import db, migrate
from os import getenv


def create_app(config_name=None):
    '''
    App fabrications function
    '''
    if config_name is None:
        config_name = getenv("FLASK_ENV", "default")

    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route('/')
    def hello():
        return 'Привет, Flask работает!'

    from .routers.questions import questions_bp
    from .routers.responses import responses_bp
    from .routers.users import users_bp
    app.register_blueprint(questions_bp)
    app.register_blueprint(responses_bp)
    app.register_blueprint(users_bp)
    return app