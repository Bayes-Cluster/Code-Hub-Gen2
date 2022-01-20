# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import eventlet
eventlet.monkey_patch()

from flask_migrate import Migrate
from sys import exit
from decouple import config

from modules.config import config_dict
from modules import create_app, db, socketio


# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)
# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'
try:
    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]
except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)

if DEBUG==False:
    app.logger.info('DEBUG       = ' + str(DEBUG))
    app.logger.info('Environment = ' + get_config_mode)
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI)


if __name__ == "__main__":
    socketio.run(app, port=5000, host="127.0.0.1")
    #app.run(port=5000)
    """
    before run, create a database in your local machine:
    `CREATE DATABASE codehub CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;`
    to start: gunicorn --bind 127.0.0.1:5000 run:app
    """
