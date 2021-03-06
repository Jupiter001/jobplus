from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from jobplus.models import (db, User)
from jobplus.config import configs


def register_extensions(app):
    db.init_app(app)
    Migrate(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    login_manager.login_view = 'front.login'


def register_blueprints(app):
    from .handlers import admin, company, front, job
    app.register_blueprint(admin)
    app.register_blueprint(company)
    app.register_blueprint(front)
    app.register_blueprint(job)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(configs.get(config))

    register_extensions(app)
    register_blueprints(app)

    return app
