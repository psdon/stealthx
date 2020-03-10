import json
from base64 import b64encode

import requests
from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
from sentry_sdk import capture_exception

from stealthx.auth.utils import send_confirm_email
from stealthx.constants import subscription_plan, RSA_PUB_KEY
from stealthx.extensions import db
from stealthx.library.rsa import import_key, encrypt
from stealthx.models import PaymongoPaymentTransaction, SubscriptionPlan, User, CDat
from stealthx.watcher import register_watchers
from .forms import CheckoutPlanForm, AccountSettingsForm, ChangePasswordForm, PersonalInformationForm, CheckoutTokenForm

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


@bp.route("/checkout/card/plan", methods=["GET", "POST"])
def checkout_card_plan():
    subscription_obj = SubscriptionPlan.query.filter_by(user_id=current_user.id) \
        .order_by(SubscriptionPlan.id.desc()).first()

    # if subscription_obj.type == subscription_plan.STARTER_PACK.type:
    #     return redirect(url_for('account.dashboard'))

    form = CheckoutPlanForm()

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
        timestamp = resp_json['data']['attributes']['created_at']
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
            capture_exception(error)
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
            capture_exception(error)
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.checkout_card'))

        return redirect(url_for('account.dashboard'))

    return render_template("account/checkout/card_monthly/index.html", form=form)


@bp.route("/checkout/card/token", methods=['GET', 'POST'])
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

        data = {
            "data": {
                "attributes": {
                    "amount": int(f"{total}00"),
                    "currency": "PHP",
                    "description": f"Payment by {current_user.id}::{current_user.username} -- {form.token.data} token",
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
                                               credited_token=form.token.data,
                                               user=current_user)
        trans_obj.set_datetime_from_timestamp(timestamp)

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


@bp.route("/checkout/others/")
def checkout_others():
    return render_template("account/checkout/others/index.html")


@bp.route("/settings/", methods=["GET", "POST"])
def settings():
    form = AccountSettingsForm()
    if form.validate_on_submit():
        user_obj = User.query.get(current_user.id)

        email_changed = False
        if user_obj.email != form.email.data:
            user_obj.email = form.email.data
            user_obj.email_confirmed = False
            email_changed = True

        username_changed = False
        if user_obj.username != form.username.data:
            user_obj.username = form.username.data
            username_changed = True

        if not (email_changed or username_changed):
            flash("Nothing changed!", "success")
            return redirect(url_for('account.settings'))

        try:
            db.session.commit()

            if email_changed:
                send_confirm_email(form.email.data)

            flash("You have saved it successfully!", "success")
            return redirect(url_for('account.settings'))
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            capture_exception(error)
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.settings'))
    else:
        if not form.username.data:
            form.username.data = current_user.username

        if not form.email.data:
            form.email.data = current_user.email

    return render_template("account/settings/index.html", form=form)


@bp.route("/change-password/", methods=["GET", "POST"])
def change_password():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        user_obj = User.query.get(current_user.id)
        user_obj.set_password(form.new_password.data)

        try:
            db.session.commit()
            flash("You have changed your password successfully!", "success")
            return redirect(url_for("account.settings"))
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            capture_exception(error)
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('account.settings'))

    return render_template("account/change_password/index.html", form=form)


@bp.route("/personal-information/", methods=["GET", "POST"])
def personal_information():
    form = PersonalInformationForm()
    if form.validate_on_submit():
        pass

    return render_template("account/personal_information/index.html", form=form)
