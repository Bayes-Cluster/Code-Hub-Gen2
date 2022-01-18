from distutils.log import Log
import jwt
import datetime

from functools import wraps

from apps.dashboard import blueprint
from apps.authentication.models import Users

from flask import request
from flask import redirect, url_for, session
from flask import Flask, jsonify, render_template, make_response
from apps.config import secret_key, exp_time

from apps.utils.token import *
from apps.config import secret_key, exp_time

@blueprint.route("/dashboard")
@token_required
def dashboard():
    username = request.cookies.get('username')
    return render_template('main/dashboard.html', name=username, token=request.args["token"])

# TODO: Add bokeh dashboard
"""
@blueprint.route("/dashboard_data")
@token_required
def dashboard_data():
    ...
"""