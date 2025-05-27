# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(3, 80)])
    password = PasswordField("Password", validators=[DataRequired(), Length(6, 128)])
    confirm  = PasswordField("Confirm",  validators=[DataRequired(), EqualTo("password")])
    submit   = SubmitField("Sign Up")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit   = SubmitField("Log In")
