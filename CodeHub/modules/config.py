# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import os
import platform
from decouple import config
from configparser import ConfigParser

BASE_DIR = os.path.dirname(__file__)
__SETTINGS_PATH__ = os.path.join(BASE_DIR, "config.ini")

def get_db_conf():
    config = ConfigParser()
    config.read(__SETTINGS_PATH__)
    return config


secret_key = '2zl0cJDDYy3FtChHu5U28Sn19aEXMj1Raz27Eld7gnU='# generate_secret(keylength=32)
exp_time = int(1800)

class Config(object):

    basedir = os.path.abspath(os.path.dirname(__file__))

    # Set up the App SECRET_KEY
    SECRET_KEY = config('SECRET_KEY', default="{}".format(secret_key))
    EXP_TIME= config("EXP_TIME", exp_time)
    fd = config("fd", None)
    SESSION_TYPE = config("SESSION_TYPE", "filesystem")
    child_pid = config("child_pid", None)
    MAIL_SUPPORT_EMAIL = config("MAIL_SUPPORT_EMAIL", "bayes@uicstat.com")
    # This will create a file in <app> FOLDER
    if platform.system() == "Windows":
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
    elif platform.system() == "Linux":
        SQLALCHEMY_DATABASE_URI = 'sqlite:////' + os.path.join(basedir, 'db.sqlite3')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    


class ProductionConfig(Config):
    DEBUG = False
    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600
    # PostgreSQL database
    SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}:{}/{}'.format(
        config('DB_ENGINE', default='mariadb+mariadbconnector'),
        config('DB_USERNAME', default='codehub'),
        config('DB_PASS', default='password'),
        config('DB_HOST', default='localhost'),
        config('DB_PORT', default=3306),
        config('DB_NAME', default='CodeHub')
    )


class DebugConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    'Production': ProductionConfig,
    'Debug': DebugConfig
}
