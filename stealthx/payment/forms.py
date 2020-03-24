from datetime import datetime

from flask_login import current_user
from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, DateField, IntegerField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import pycountry
import phonenumbers

from stealthx.models import User

tokens = [(100, 100), (300, 300), (500, 500), (1000, 1000)]


class CheckoutTokenForm(FlaskForm):
    token = SelectField(default=100, choices=tokens, validators=[DataRequired(message="Enter token amount")], coerce=int)

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


class CheckoutPlanForm(FlaskForm):
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
