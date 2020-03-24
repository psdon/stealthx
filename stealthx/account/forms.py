import phonenumbers
import pycountry
from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo

from stealthx.models import User

countries = [("Country", "Country")]

for country in pycountry.countries:
    countries.append((country.name, country.name))


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
    current_password = PasswordField(validators=[DataRequired(message="Current password is a required field"), ])

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


class PersonalInformationForm(FlaskForm):
    first_name = StringField(validators=[DataRequired(message="Enter your first name")])
    middle_name = StringField(validators=[DataRequired(message="Enter your middle name")])
    last_name = StringField(validators=[DataRequired(message="Enter your last name")])
    mobile = StringField(validators=[DataRequired(message="Enter your mobile number")])
    address1 = StringField(validators=[DataRequired(message="Enter your house, unit #")])
    address2 = StringField(validators=[DataRequired(message="Enter your street address")])
    region = StringField(validators=[DataRequired(message="Enter your province, region or county")])
    city = StringField(validators=[DataRequired(message="Enter your city address")])
    zip_code = StringField(validators=[DataRequired(message="Enter your zip code")])

    country = SelectField(default=("Country", "Country"), choices=countries,
                          validators=[DataRequired(message="Enter your country")])

    @staticmethod
    def validate_country(_, field):
        if field.data == "Country":
            raise ValueError("Choose your country")

    @staticmethod
    def validate_zip_code(_, field):
        if not field.data.isdigit():
            raise ValueError("Enter a valid zip code")

    @staticmethod
    def validate_mobile(_, field):
        plus_sign = field.data[0:3]
        if plus_sign[0] != "+":
            raise ValueError("Enter your mobile number with country code (i.e. +63)")

        try:
            cp = phonenumbers.parse(field.data)
        except Exception as error:
            raise ValueError("Enter a valid mobile number")

        if not phonenumbers.is_valid_number(cp):
            raise ValueError("Enter a valid mobile number")
