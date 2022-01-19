import jwt
import datetime
import pyqrcode
from io import BytesIO

from modules.authentication import blueprint
from modules.authentication.auth import *
from modules.authentication.forms import *
from modules.authentication.models import Users, HomeDirectory

from flask import request
from flask import redirect, url_for, flash
from flask import Flask, jsonify, render_template, make_response

from modules.utils.token import *
from modules.config import secret_key, exp_time
"""
import os, base64
generate secret key
def generate_secret():
    return base64.b64encode(os.urandom(32)).decode("ascii")
"""


@blueprint.route('/')
def homepage():
    if check_token_expired(request.cookies.get("token")) == False:
        access_token = token_generate(
            access=True, data={"username": request.cookies.get("username")})
        return render_template("main/homepage.html",
                               username=request.cookies.get("username"),
                               token=access_token)
    else:
        return render_template("main/homepage.html")

    return render_template(
        "main/homepage.html"
    )  #redirect(url_for('authentication_blueprint.login'))


@blueprint.route("/register", methods=["GET", "POST"])
def register():
    register_form = RegisterForm(request.form)
    if request.method == "POST":
        username = register_form.username.data
        password = register_form.password.data
        user = Users.query.filter_by(username=username).first()
        if user is not None:
            msg = "Username already exists"
            return redirect(url_for("authentication_blueprint.login", msg=msg))
        else:
            if username == "" and password == "":
                msg = "Username and password are required"
                return render_template("accounts/register.html", msg=msg)
            if "@" in username:
                verification = auth_ldap(username, password, mail=True)
            else:
                verification = auth_ldap(username, password, mail=False)
            if verification:
                user = Users(username=username, password=password)
                db.session.add(user)
                db.session.commit()
                return redirect(
                    url_for("authentication_blueprint.mfa", username=username))
            else:
                flash("Username or password is incorrect")
                return redirect(url_for("authentication_blueprint.register"))
    return render_template("accounts/register.html", form=register_form)


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    msg = None
    login_form = LoginForm(request.form)
    if request.method == "POST":
        username = login_form.username.data
        password = login_form.password.data
        mfa_token = login_form.mfa_token.data

        if username == "" and password == "":
            msg = "Username and password are required"
            return render_template("accounts/login.html", msg=msg)
        if "@" in username:
            verification = auth_ldap(username, password, mail=True)
        else:
            verification = auth_ldap(username, password, mail=False)
        if verification == True:
            access_token = token_generate(access=True,
                                          data={"username": username})
            refresh_token = token_generate(access=False,
                                           data={"username": username})
            home_directory = find_user_directory(uid=username)
            resp = make_response(
                redirect(
                    url_for("dashboard_blueprint.dashboard",
                            token=access_token)))
            resp.set_cookie("token", refresh_token)
            resp.set_cookie("username", username)
            #resp.set_cookie("password", "{}".format(password)) ## warning: this is not secure
            user = Users.query.filter_by(
                username=login_form.username.data).first()
            verification_mfa = user.auth_totp(mfa_token=mfa_token)
            if verification_mfa:
                user_form = HomeDirectory(username=username,
                                          homepath=home_directory)
                db.session.add(user_form)
                db.session.commit()
                return resp
        else:
            msg = "Invalid username or password"
            return render_template("accounts/login.html",
                                   msg=msg,
                                   form=login_form)
    return render_template("accounts/login.html", msg=msg, form=login_form)


@blueprint.route("/mfa")
@check_token_revoke
def mfa():
    username = request.args["username"]
    return render_template("accounts/mfa.html", username=username)


@blueprint.route("/qrcode")
def qrcode():
    username = request.cookies.get("username")
    user = Users.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    }


## TODO: Design a database for user and store token whether the token is valid or not
@blueprint.route("/logout", methods=["GET", "POST"])
@token_required
def logout(*args):
    access_token = request.args["token"]
    refresh_token = request.cookies.get("token")
    db.session.add(
        TokenBlocklist(type="access",
                       token=access_token,
                       create_time=datetime.datetime.now()))
    db.session.add(
        TokenBlocklist(type="refresh",
                       token=refresh_token,
                       create_time=datetime.datetime.now()))
    db.session.commit()
    return redirect(url_for('authentication_blueprint.login'))