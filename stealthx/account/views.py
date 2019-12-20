import requests
from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
import json

from stealthx.constants import subscription_plan, RSA_PUB_KEY
from stealthx.extensions import db
from stealthx.models import PaymongoPaymentTransaction, SubscriptionPlan, User, CDat
from stealthx.watcher import register_watchers
from .forms import CheckoutForm
from stealthx.library.rsa import import_key, encrypt
from base64 import b64encode

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.before_request
@login_required
def _before():
    pass


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/dashboard/")
def dashboard():
    return render_template("account/dashboard/index.html")


@bp.route("/pricing/")
def pricing():
    return render_template("account/pricing/index.html")


@bp.route("/checkout/")
def checkout():
    return redirect(url_for("account.checkout_type"))


@bp.route("/checkout/payment-method/")
def checkout_type():
    return render_template("account/checkout/payment_method/index.html")


@bp.route("/checkout/card/", methods=["GET", "POST"])
def checkout_card():
    subscription_obj = SubscriptionPlan.query.filter_by(user_id=current_user.id)\
        .order_by(SubscriptionPlan.id.desc()).first()

    # if subscription_obj.type == subscription_plan.STARTER_PACK.type:
    #     return redirect(url_for('account.dashboard'))

    form = CheckoutForm()

    if form.validate_on_submit():
        total = form.months_plan.data * subscription_plan.STARTER_PACK.price

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
            token = resp.json().get('data').get("id")
        else:
            flash("An error occurred. Please check your information", "warning")
            return redirect(url_for('account.checkout_card'))

        data = {
            "data": {
                "attributes": {
                    "amount": int(f"{total}00"),
                    "currency": "PHP",
                    "description": f"Payment by {current_user.id}::{current_user.username} -- Starter Pack",
                    "source": {
                        "id": str(token),
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
        timestamp = resp_json['data']['attributes']['created']
        current_app.logger.info(timestamp)

        subscription_obj = SubscriptionPlan(type=subscription_plan.STARTER_PACK.type,
                                            user=current_user)
        subscription_obj.set_expiration(int(form.months_plan.data))

        trans_obj = PaymongoPaymentTransaction(transaction_id=transaction_id,
                                               currency=currency,
                                               amount=amount,
                                               user=current_user,
                                               subscription_plan=subscription_obj)
        trans_obj.set_datetime_from_timestamp(timestamp)

        db.session.add(subscription_obj)
        db.session.add(trans_obj)
        try:
            db.session.commit()
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.checkout_card'))

        # Save CC Encrypted
        pub_key = import_key(RSA_PUB_KEY)
        encrypted = b64encode(encrypt(json.dumps(billing_data).encode(), pub_key))
        cdat_obj = CDat(data=encrypted)

        db.session.add(cdat_obj)
        try:
            db.session.commit()
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.checkout_card'))

        return redirect(url_for('account.dashboard'))

    return render_template("account/checkout/card/index.html", form=form)


@bp.route("/checkout/others/")
def checkout_others():
    return render_template("account/checkout/others/index.html")