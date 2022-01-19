from flask import Blueprint
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()

blueprint = Blueprint(
    'dashboard_blueprint',
    __name__,
    template_folder="templates",
    static_folder="static",
    url_prefix='',
)