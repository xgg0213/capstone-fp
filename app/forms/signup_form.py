from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, ValidationError, Length
from app.models import User


def user_exists(form, field):
    # Checking if user exists
    email = field.data
    user = User.query.filter(User.email == email).first()
    if user:
        raise ValidationError('Email address is already in use.')


def username_exists(form, field):
    # Checking if username is already in use
    username = field.data
    user = User.query.filter(User.username == username).first()
    if user:
        raise ValidationError('Username is already in use.')


class SignUpForm(FlaskForm):
    username = StringField('username', validators=[
        DataRequired(), 
        Length(min=4, message='Username must be at least 4 characters'),
        username_exists
    ])
    email = StringField('email', validators=[
        DataRequired(), 
        Email(message='Please enter a valid email'),
        user_exists
    ])
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters')
    ])
