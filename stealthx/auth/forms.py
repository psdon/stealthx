# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from stealthx.models import User


class SignInForm(FlaskForm):
    """Login form."""

    username_or_email = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class SignUpForm(FlaskForm):
    """Register form."""

    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is a required field"),
            Length(min=3, max=25),
        ],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Email is a required field"),
            Email(),
            Length(min=6, max=40),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is a required field"),
            Length(min=8),
        ],
    )
    confirm = PasswordField(
        "Verify password",
        [
            DataRequired(message="Confirm password is a required field"),
            EqualTo("password", message="Password does not match"),
        ],
    )

    @staticmethod
    def validate_username(_, field):
        has_user = User.query.filter_by(username=field.data).first()
        if has_user:
            raise ValueError("This username is taken")

    @staticmethod
    def validate_email(_, field):
        has_user = User.query.filter_by(email=field.data).first()
        if has_user:
            raise ValueError("This email is already registered")


class RecoverForm(FlaskForm):
    email = StringField(
        "Username",
        validators=[DataRequired(message="Email is a required field"), Email()],
    )


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is a required field"),
            Length(min=8),
        ],
    )
    confirm = PasswordField(
        "Verify password",
        [
            DataRequired(message="Confirm password is a required field"),
            EqualTo("password", message="Password does not match"),
        ],
    )


class ChangeEmailForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Enter a valid email address"),
            Email(),
            Length(min=6, max=40),
        ],
    )

    @staticmethod
    def validate_email(_, field):
        has_user = User.query.filter_by(email=field.data).first()
        if has_user:
            raise ValueError("This email is already registered")