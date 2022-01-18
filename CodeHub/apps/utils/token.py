import jwt
from flask import request, jsonify, redirect, url_for
from functools import wraps
from apps.config import secret_key, exp_time

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