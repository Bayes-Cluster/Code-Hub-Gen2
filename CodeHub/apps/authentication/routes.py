import jwt
import datetime

from functools import wraps
from flask import request
from apps.authentication import blueprint
from apps.authentication.auth import *
from flask import Flask, jsonify, render_template
from flask import  redirect, url_for

SECRET_KEY = "8QAJbYIlGEjN52MhkAytpLH0qPHcx9SbizUVMN7JJrc="
EXP_TIME = int(600)

"""
import os, base64
generate secret key
def generate_secret():
    return base64.b64encode(os.urandom(32)).decode("ascii")
"""

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get(
            "token")  # http://127.0.0.1:5000/route?token={token}
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        else:
            try:
                data = jwt.decode(token,
                                  SECRET_KEY,
                                  algorithms=["HS256"])
            except Exception as e:
                return jsonify({"message": "Token is invalid"}), 401

            return f(*args, **kwargs)

    return decorated


@blueprint.route('/')
def homepage():
    return redirect(url_for('authentication_blueprint.login'))

@blueprint.route("/login", methods=["GET", "POST"])
def login():
    login_error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "" or password == "":
            login_error = "Username or password is missing"
            return render_template("accounts/login.html", login_error=login_error)
        if "@" in username:
            auth_result = auth_ldap(username, password, mail=True)
        else:
            auth_result = auth_ldap(username, password, mail=False)
        if auth_result == True:
            token = jwt.encode(
                {
                    "user":
                    username,
                    "exp":
                    datetime.datetime.utcnow() +
                    datetime.timedelta(seconds=EXP_TIME)
                }, SECRET_KEY)
            return redirect("/profile?token={}".format(token))
        else:
            login_error = "Invalid username or password"
            return render_template("accounts/login.html", login_error=login_error)
    return render_template("accounts/login.html", login_error=login_error)


@blueprint.route("/profile", methods=["GET", "POST"])
@token_required
def profile(*args):
    token = request.args['token']
    username = jwt.decode(token,
                          SECRET_KEY,
                          algorithms=["HS256"])['user']
    username = request.form.get("username")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    if old_password == None or new_password == None or old_password == new_password:
        modify_notice = "Invlid password or new password is same as current password"
        modify_result = False
        return render_template("accounts/profile.html",
                               modify_result=False,
                               modify_notice=modify_notice)
    modify_result = change_password_ldap(username, old_password, new_password)
    if modify_result == True:
        return render_template("accounts/profile.html", modify_result=modify_result)

    return render_template("accounts/profile.html", username = username)
