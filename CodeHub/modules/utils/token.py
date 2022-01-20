import jwt
import datetime
from functools import wraps
from modules import authentication
from modules.authentication.models import TokenBlocklist
from modules import db
from modules.config import secret_key, exp_time
from modules.authentication.models import TokenBlocklist
from flask import render_template, request, jsonify, redirect, url_for, abort

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            msg = "Token is missing, please login again"
            return render_template("accounts/login.html", msg=msg)

        try: 
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
        except:
            msg = "Token is invlid, please login again!"
            return redirect(url_for("authentication_blueprint.login", msg=msg))

        return f(*args, **kwargs)

    return decorator

def token_generate(access:bool=True, data:dict=None):
    if access == True:
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # 30 minutes
        token = jwt.encode({
            "username": data["username"],
            "exp": exp,
        }, secret_key, algorithm="HS256")
        if TokenBlocklist.query.filter_by(token=token).first() is not None:
            return token_generate(access=True, data=data)
        else:
            return token

    else:
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=720) # 12 hours
        token = jwt.encode({
            "username": data["username"],
            "exp": exp,
        }, secret_key, algorithm="HS512")
        if TokenBlocklist.query.filter_by(token=token).first() is not None:
            return token_generate(access=True, data=data)
        else:
            return token

def token_renew(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        username = request.cookies.get("username")
        refresh_token = request.cookies.get("token")
        access_token = request.args["token"]
        try:
            check_access_exp = check_token_expired(access_token)
        except:
            return redirect(url_for("authentication_blueprint.login", msg="Access Token is invalid, please login again"))
        if check_access_exp: 
            try:
                token_info = jwt.decode(refresh_token, secret_key, algorithms=["HS512"])["username"]
            except:
                return redirect(url_for("authentication_blueprint.login", msg="Refresh token is invalid, please login again"))
            if token_info == username:
                access_token = token_generate(access=True, data={"username": username})
            else:
                return redirect(url_for("authentication_blueprint.login", msg="Invalid username, please login again"))
        else:
            access_token = access_token
        return f(*args, **kwargs, token=access_token)
    return decorator

def check_token_expired(token:str=None) -> bool:
    try:
        data = jwt.decode(token, secret_key, algorithms=["HS256"])
    except:
        return True
    if data["exp"] < datetime.datetime.utcnow().timestamp():
        return True
    else:
        return False


def token_revoked(token:str=None):
    revoked = db.session.query(TokenBlocklist.id).filter(TokenBlocklist.token == token).scalar()
    return revoked

def check_token_revoke(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        access_token = request.args.get('token')
        refresh_token = request.cookies.get("token")
        if token_revoked(access_token):
            return redirect(url_for("authentication_blueprint.login", msg="Access Token is revoked, please login again"))
        elif token_revoked(access_token):
            return redirect(url_for("authentication_blueprint.login", msg="Refresh Token is revoked, please login again"))

        return f(*args, **kwargs)
    return decorator


