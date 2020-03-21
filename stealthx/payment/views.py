from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from stealthx.models import PaymongoPaymentTransaction
from sentry_sdk import capture_exception
import requests

from stealthx.extensions import db

from .forms import CheckoutTokenForm

bp = Blueprint("payment", __name__, url_prefix="/payment")


@bp.before_request
@login_required
def _before():
    pass


@bp.route("/card/token", methods=['GET', 'POST'])
def checkout_card_token():

    form = CheckoutTokenForm()
    token_price = 1

    if form.validate_on_submit():
        total = form.token.data * token_price

        billing_data = {
            "data": {
                "attributes": {
                    "number": str(form.number.data),
                    "exp_month": int(form.date.data.strftime("%m")),
                    "exp_year": int(form.date.data.strftime("%y")),
                    "cvc": str(form.cvv.data),
                    "billing": {
                        "name": str(form.name.data),
                        "email": current_user.email
                    }
                }
            }
        }

        resp = requests.post("https://api.paymongo.com/v1/tokens",
                             auth=(current_app.config.get("PAYMONGO_PUBLIC_KEY"), ""),
                             json=billing_data)

        if resp.status_code == 201:
            token_obj_id = resp.json().get('data').get("id")
        else:
            flash("An error occurred. Please check your information", "warning")
            return redirect(url_for('account.checkout_card'))

        token_amount = form.token.data

        data = {
            "data": {
                "attributes": {
                    "amount": int(f"{total}00"),
                    "currency": "PHP",
                    "description": f"Payment by {current_user.id}::{current_user.username} -- {token_amount} token",
                    "source": {
                        "id": str(token_obj_id),
                        "type": "token"
                    }
                }
            }
        }

        resp = requests.post("https://api.paymongo.com/v1/payments",
                             auth=(current_app.config.get("PAYMONGO_SECRET_KEY"), ""),
                             json=data)

        if resp.status_code == 201:
            current_app.logger.info("Transaction Successful")
        else:
            flash("An error occurred. Please check your information", "warning")
            return redirect(url_for('account.checkout_card'))

        resp_json = resp.json()

        transaction_id = resp_json['data']['id']
        currency = resp_json['data']['attributes']['currency']
        amount = resp_json['data']['attributes']['amount']
        timestamp = resp_json['data']['attributes']['created_at']
        current_app.logger.info(timestamp)

        trans_obj = PaymongoPaymentTransaction(transaction_id=transaction_id,
                                               currency=currency,
                                               amount=amount,
                                               credited_token=token_amount,
                                               user=current_user)
        trans_obj.set_datetime_from_timestamp(timestamp)
        current_user.core.token = current_user.core.token + token_amount

        db.session.add(trans_obj)
        try:
            db.session.commit()
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            capture_exception(error)
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.checkout_card'))

    return render_template("account/checkout/card_token/index.html", form=form, token_price=token_price)
