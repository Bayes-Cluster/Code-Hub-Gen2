from apps import *
from flask import Flask
from flask_session import Session
from importlib import import_module
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO


db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO(async_mode="eventlet")


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)



def register_blueprints(app):
    for module_name in ('authentication', 'main'):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)


def configure_database(app):

    @app.before_first_request
    def initialize_database():
        db.create_all()


def create_app(config):
    main_app = Flask(__name__)
    main_app.config.from_object(config)
    register_extensions(main_app)
    register_blueprints(main_app)
    bootstrap = Bootstrap(main_app)
    db = SQLAlchemy(main_app)
    socketio = SocketIO(main_app)
    login_manager.init_app(main_app)
    login_manager.login_view = 'login'
    configure_database(main_app)
    return main_app
