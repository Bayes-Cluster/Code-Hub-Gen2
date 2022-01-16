from distutils.log import Log
import jwt
import datetime

from functools import wraps

from apps.authentication import blueprint
from apps.authentication.auth import *
from apps.authentication.forms import *

from flask import request
from flask import  redirect, url_for
from flask import Flask, jsonify, render_template, make_response

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
    msg = None
    login_form = LoginForm(request.form)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == "" and password == "":
            msg = "Username and password are required"
            return render_template("accounts/login.html", msg = msg)
        if "@" in username:
            verification = auth_ldap(username, password, mail=True)
        else:
            verification = auth_ldap(username, password, mail=False)
        if verification == True:
            token = jwt.encode(
                {
                    "user":
                    username,
                    "exp":
                    datetime.datetime.utcnow() +
                    datetime.timedelta(seconds=EXP_TIME)
                }, SECRET_KEY)
            resp = make_response(redirect("profile?token={}".format(token)))
            resp.set_cookie('username', username)
            resp.set_cookie("password", "{}".format(password)) 
            return resp
        else:
            msg = "Invalid username or password"
            return render_template("accounts/login.html", msg=msg, form = login_form)
    return render_template("accounts/login.html", msg=msg, form=login_form)

@blueprint.route("/profile", methods=["GET", "POST"])
@token_required
def profile(*args):
    token = request.args['token']
    username = jwt.decode(token,
                          SECRET_KEY,
                          algorithms=["HS256"])['user']
    username = request.cookies.get('username')
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
        return redirect("/logout?token={}".format(token))

    return render_template("accounts/profile.html", username = username)

## TODO: Design a database for user and store token whether the token is valid or not
@blueprint.route("/logout", methods=["GET", "POST"])
@token_required
def logout(*args):
    token = request.args['token']
    return jsonify({"token":token})