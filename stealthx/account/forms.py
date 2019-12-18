from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, DecimalField, DateField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length

from flask import current_app
from datetime import datetime

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

