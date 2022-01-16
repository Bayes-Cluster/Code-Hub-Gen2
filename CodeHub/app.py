from importlib_metadata import re
import jwt
import datetime
from auth.auth import *
from functools import wraps
from flask import Flask, jsonify, render_template, render_template_string
from flask import make_response, redirect, url_for, flash, abort
from flask import request, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "8QAJbYIlGEjN52MhkAytpLH0qPHcx9SbizUVMN7JJrc="
app.config["EXP_TIME"] = int(600)
"""
import os, base64
generate secret key
def generate_secret():
    return base64.b64encode(os.urandom(32)).decode("ascii")
"""

"""
error handler
"""

@app.errorhandler(401)
def page_unauthorized(error):
    return render_template_string('<h1> Unauthorized </h1><h2>{{ error_info }}</h2>', error_info=error), 401

@app.errorhandler(404)
def page_not_found(error):
    return render_template_string('<h1> Page Not Found </h1><h2>{{ error_info }}</h2>', error_info=error), 404
    

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
                                  app.config["SECRET_KEY"],
                                  algorithms=["HS256"])
            except Exception as e:
                return jsonify({"message": "Token is invalid"}), 401

            return f(*args, **kwargs)

    return decorated


@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == "" or password == "":
            login_error = "Username or password is missing"
            return render_template("login.html", login_error=login_error)
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
                    datetime.timedelta(seconds=app.config["EXP_TIME"])
                }, app.config["SECRET_KEY"])
            return redirect("/profile?token={}".format(token))
        else:
            login_error = "Invalid username or password"
            return render_template("login.html", login_error=login_error)
    return render_template("login.html")


@app.route("/profile", methods=["GET", "POST"])
@token_required
def profile(*args):
    token = request.args['token']
    username = jwt.decode(token,
                          app.config["SECRET_KEY"],
                          algorithms=["HS256"])['user']
    username = request.form.get("username")
    old_password = request.form.get("old_password")
    new_password = request.form.get("new_password")
    if old_password == None or new_password == None or old_password == new_password:
        modify_notice = "Invlid password or new password is same as current password"
        modify_result = False
        return render_template("profile.html",
                               modify_result=False,
                               modify_notice=modify_notice)
    modify_result = change_password_ldap(username, old_password, new_password)
    if modify_result == True:
        return render_template("profile.html", modify_result=modify_result)

    return render_template("profile.html", username = username)


if __name__ == "__main__":
    app.run(debug=True)