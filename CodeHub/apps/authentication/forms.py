"""
forms for Login and Update
"""

from cProfile import label
from wsgiref import validate
from flask_wtf import FlaskForm
from apps import authentication
from apps.authentication import *
from apps.authentication.models import *
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, BooleanField


class LoginForm(FlaskForm):
    username = StringField(label="",
                           id="username",
                           validators=[DataRequired()])
    password = PasswordField(label="",
                             id="password",
                             validators=[DataRequired()])
    remember = BooleanField(label="Remember Me", id="remember_me")


class ModifyForm(FlaskForm):
    old_password = PasswordField(label="Current Password", id="old_password", validator=[DataRequired()])
    new_password = PasswordField(label="New Password", id="new_password", validators=[DataRequired()])