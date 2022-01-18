from distutils.log import Log
import jwt
import datetime

from apps.authentication import blueprint
from apps.authentication.auth import *
from apps.authentication.forms import *
from apps.authentication.models import Users

from flask import request
from flask import redirect, url_for, session
from flask import Flask, jsonify, render_template, make_response

from apps.utils.token import *
from apps.config import secret_key, exp_time
"""
import os, base64
generate secret key
def generate_secret():
    return base64.b64encode(os.urandom(32)).decode("ascii")
"""


@blueprint.route('/')
def homepage():
    return render_template("main/homepage.html")#redirect(url_for('authentication_blueprint.login'))


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    login_form = LoginForm(request.form)
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if username == "" and password == "":
            msg = "Username and password are required"
            return render_template("accounts/login.html", msg=msg)
        if "@" in username:
            verification = auth_ldap(username, password, mail=True)
        else:
            verification = auth_ldap(username, password, mail=False)
        if verification == True:
            exp = datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_time)
            token = jwt.encode({
                "username": username,
                "exp": exp,
            }, secret_key)
            resp = make_response(redirect("dashboard?token={}".format(token)))
            resp.set_cookie('username', username)
            resp.set_cookie("password", "{}".format(password))
            user_form = Users(username=username,
                              token=token,
                              token_expiration=False)
            db.session.add(user_form)
            db.session.commit()
            return resp
        else:
            msg = "Invalid username or password"
            return render_template("accounts/login.html",
                                   msg=msg,
                                   form=login_form)
    return render_template("accounts/login.html", msg=msg, form=login_form)


@blueprint.route("/profile", methods=["GET", "POST"])
@token_required
def profile(*args):
    token = request.args['token']
    username = jwt.decode(token, secret_key, algorithms=["HS256"])["username"]
    username = request.cookies.get('username')
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    if old_password == None or new_password == None or old_password == new_password:
        msg = "Invlid password or new password is same as current password"
        modify_result = False
        return render_template("accounts/profile.html",
                               modify_result=False,
                               msg=msg)
    modify_result = change_password_ldap(username, old_password, new_password)
    if modify_result == True:
        return redirect("/logout?token={}".format(token))
    else:
        msg = "Invalid password, please re enter"
        return render_template("accounts/profile.html", msg=msg)

    return render_template("accounts/profile.html", msg=username)


## TODO: Design a database for user and store token whether the token is valid or not
@blueprint.route("/logout", methods=["GET", "POST"])
@token_required
def logout(*args):
    token = request.args["token"]
    username = jwt.decode(token, secret_key, algorithms=["HS256"])["username"]
    user_form = Users.query.filter_by(token=token).first()
    user_form.token_expiration = True
    db.session.commit()
    resp = make_response(redirect("login"))
    resp.set_cookie("username", "", expires=0)
    return redirect(url_for('authentication_blueprint.login'))