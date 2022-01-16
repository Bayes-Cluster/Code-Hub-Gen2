from cProfile import label
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError


class LoginForm(FlaskForm):
    username = StringField(label="Username or email",
                           id="username",
                           validators=[DataRequired()])
    password = PasswordField(label="Password",
                             id="password",
                             validators=[DataRequired()])
