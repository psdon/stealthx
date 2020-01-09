from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from stealthx.models import User


class CheckoutForm(FlaskForm):
    months_plan = DecimalField(validators=[DataRequired()])

    name = StringField(validators=[DataRequired(message="Enter name on card")])
    number = IntegerField(validators=[DataRequired(message="Enter a valid card number")])
    date = DateField(format="%m/%y", validators=[DataRequired(message="Enter valid expiration date")])
    cvv = IntegerField(validators=[DataRequired(message="Enter a valid CVV")])

    @staticmethod
    def validate_date(_, field):
        # Month Year Now... Day = 1
        date_now = datetime.strptime(datetime.utcnow().date().strftime("%m/%Y"), "%m/%Y").date()
        if not field.data >= date_now:
            raise ValueError("Enter a valid expiration date")


class AccountSettingsForm(FlaskForm):
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
            DataRequired(message="Enter a valid email address"),
            Email(),
            Length(min=6, max=40),
        ],
    )

    @staticmethod
    def validate_username(_, field):
        if field.data == current_user.username:
            return None

        has_user = User.query.filter_by(username=field.data).first()
        if has_user:
            raise ValueError("This username is taken")

    @staticmethod
    def validate_email(_, field):
        if field.data == current_user.email:
            return None

        has_user = User.query.filter_by(email=field.data).first()
        if has_user:
            raise ValueError("This email is already registered")


class ChangePasswordForm(FlaskForm):

    current_password = PasswordField(validators=[DataRequired(message="Current password is a required field"),])

    new_password = PasswordField(
        validators=[
            DataRequired(message="New password is a required field"),
            Length(min=8),
        ],
    )

    confirm = PasswordField(
        validators=[
            DataRequired(message="Confirm password is a required field"),
            EqualTo("new_password", message="Password does not match"),
        ],
    )

    @staticmethod
    def validate_current_password(_, field):
        if not current_user.check_password(field.data):
            raise ValueError("Incorrect password")
