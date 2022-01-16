from flask import Flask
from apps import authentication
from importlib import import_module

def register_blueprints(app):
    module = import_module('apps.{}.routes'.format("authentication"))
    app.register_blueprint(module.blueprint)


def create_app(config):
    main_app = Flask(__name__)
    main_app.config["SECRET_KEY"] = "8QAJbYIlGEjN52MhkAytpLH0qPHcx9SbizUVMN7JJrc="
    main_app.config["EXP_TIME"] = int(600)
    register_blueprints(main_app)
    return main_app
