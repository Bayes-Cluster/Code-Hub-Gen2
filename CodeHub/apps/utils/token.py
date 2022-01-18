import jwt
import datetime
from functools import wraps
from CodeHub.apps import authentication
from apps.config import secret_key, exp_time
from flask import request, jsonify, redirect, url_for, abort

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            msg = "Token is invlid"
            return redirect(url_for("authentication_blueprint.login", msg = msg))

        try: 
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

def token_generate(access:bool=True, data:dict=None):
    if access == True:
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=30) # 30 minutes
        token = jwt.encode({
            "username": data["username"],
            "exp": exp,
        }, secret_key, algorithm="HS256")
        return token
    else:
        exp = datetime.datetime.utcnow() + datetime.timedelta(minutes=720) # 12 hours
        token = jwt.encode({
            "username": data["username"],
            "exp": exp,
        }, secret_key, algorithm="HS512")
        return token

def token_renew():
    username = request.cookies.get('username')
    refresh_token = request.cookies.get('refresh_token')
    try:
        token_info = jwt.decode(refresh_token, secret_key, algorithms=["HS512"])
    except:
        abort(403)
    if token_info == username:
        access_token = token_generate(access=True, data={"username": username})
        return access_token
    else:
        return redirect(url_for("authentication_blueprint.login"))
