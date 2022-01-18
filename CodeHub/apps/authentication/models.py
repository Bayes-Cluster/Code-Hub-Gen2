"""
Database for validate user token
"""

from flask_login import UserMixin
from apps import db, login_manager
#from apps.authentication.util import hash_pass


class Users(db.Model, UserMixin):

    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=False)
    token = db.Column(db.String(128), unique=True)
    token_expiration = db.Column(db.Boolean, unique=False, default=False)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))