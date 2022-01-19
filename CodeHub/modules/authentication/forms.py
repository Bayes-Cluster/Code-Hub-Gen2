"""
forms for Login and Update
"""

from cProfile import label
from wsgiref import validate
from flask_wtf import FlaskForm
from modules import authentication
from modules.authentication import *
from modules.authentication.models import *
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class RegisterForm(FlaskForm):
    """Register Form"""
    username = StringField(label="",
                           id="username",
                           validators=[DataRequired()])
    password = PasswordField(label="",
                             id="password",
                             validators=[DataRequired()])
    submit = SubmitField(label="", id="register")


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField(label="",
                           id="username",
                           validators=[DataRequired()])
    password = PasswordField(label="",
                             id="password",
                             validators=[DataRequired()])
    mfa_token = PasswordField(label="",
                              id="mfa_token",
                              validators=[DataRequired()])
    remember = BooleanField(label="Remember Me", id="remember")


class ModifyForm(FlaskForm):
    old_password = PasswordField(label="Current Password",
                                 id="old_password",
                                 validator=[DataRequired()])
    new_password = PasswordField(label="New Password",
                                 id="new_password",
                                 validators=[DataRequired()])
