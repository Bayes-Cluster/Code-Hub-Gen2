"""
Database for validate user token
"""
import os, base64
import onetimepass
from flask_login import UserMixin
from modules import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
#from modules.authentication.util import hash_pass


class Users(db.Model, UserMixin):

    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(128), unique=False)
    mfa_token = db.Column(db.String(16))

    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)
        self.mfa_token = base64.b32encode(os.urandom(10)).decode('utf-8')

    def get_totp_uri(self):
            return "otpauth://totp/USBC-2FA:{0}?secret={1}&issuer=USBC".format(self.username, self.mfa_token)
    
    def auth_totp(self, mfa_token:str):
        return onetimepass.valid_totp(mfa_token, self.mfa_token)


class TokenBlocklist(db.Model):

    __tablename__ = 'TokenBlocklist'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10), unique=False)
    token = db.Column(db.String(256), unique=True)
    create_time = db.Column(db.DateTime, unique=False)

class HomeDirectory(db.Model):
    __tablename__ = "HomeDirectory"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=False)
    homepath = db.Column(db.String(64), unique=False)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))