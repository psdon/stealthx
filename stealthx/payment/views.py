import requests
from flask import Blueprint, flash, redirect, render_template, url_for, current_app
from flask_login import current_user

from stealthx.daos import inter_dao
from stealthx.library.helper import auth_required
from stealthx.models import SubscriptionType
from stealthx.watchers.watcher import register_watchers
from .forms import CheckoutPlanForm
from .services import process_paymongo_token, process_paymongo_payment

bp = Blueprint("payment", __name__)


@bp.before_request
@auth_required
def _before():
    pass


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/pricing/")
def pricing():
    return render_template("payment/pricing/index.html")


@bp.route("/checkout/payment-method/plan/<plan>")
def checkout_type_plan(plan):
    return render_template("payment/checkout/payment_method/index.html", plan=plan)


@bp.route("/checkout/card/plan/<plan>", methods=["GET", "POST"])
def checkout_card_plan(plan):
    # Check if param is valid
    subscription_types = SubscriptionType.query.with_entities(SubscriptionType.name).all()

    valid_plan = False
    for sub in subscription_types:
        if plan in sub:
            valid_plan = True
            break

    if not valid_plan:
        return redirect(url_for("payment.pricing"))

    # Check if student
    if current_user.subscription.is_student:
        subscription_price = SubscriptionType.query.filter_by(name=plan).first().student_price
    else:
        subscription_price = SubscriptionType.query.filter_by(name=plan).first().price

    form = CheckoutPlanForm()

    if form.validate_on_submit():

        total_price = form.months_plan.data * subscription_price

        token_id = process_paymongo_token(form)
        if token_id is None:
            flash("Payment declined. Please check your information.", "warning")
            return redirect(url_for('payment.checkout_card_plan', plan=plan))

        transaction_info = process_paymongo_payment(amount=total_price, token_id=token_id, plan=plan)

        if transaction_info is None:
            # TODO: Capture this error on Sentry
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('payment.checkout_card_plan', plan=plan))

        inter_dao.subscribe_and_transact(plan=plan,
                                         duration_months=form.months_plan.data,
                                         paymongo_timestamp=transaction_info['timestamp'],
                                         transaction_id=transaction_info['id'],
                                         currency=transaction_info["currency"],
                                         amount=transaction_info['amount'],
                                         )

        commit_success = inter_dao.commit()
        if not commit_success:
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('payment.checkout_card_plan', plan=plan))

        # TODO: CDat DAO

        return redirect(url_for('account.subscription'))

    return render_template("payment/checkout/card_monthly/index.html", form=form, monthly_price=subscription_price)


@bp.route("/checkout/others/")
def checkout_others():
    return render_template("payment/checkout/others/index.html")


@bp.route("/test-new-payment")
def test_new_payment():
    # Create Payment Intent
    payment_intent_data = {
        "data": {
            "attributes": {
                "amount": 10000,
                "currency": "PHP",
                "payment_method_allowed": ['card']
            }
        }
    }

    resp = requests.post("https://api.paymongo.com/v1/payment_intents",
                         auth=(current_app.config.get("PAYMONGO_SECRET_KEY"), ""),
                         json=payment_intent_data)

    payment_intent_id = resp.json()['data']['id']

    current_app.logger.debug(f"payment_intent_id: {payment_intent_id}")

    # Create Payment Method
    payment_method_data = {
        "data": {
            "attributes": {
                "type": "card",
                "details": {
                    "card_number": "4120000000000007",
                    "exp_month": 2,
                    "exp_year": 22,
                    "cvc": "222",
                }
            }
        }
    }

    resp = requests.post("https://api.paymongo.com/v1/payment_methods",
                         auth=(current_app.config.get("PAYMONGO_PUBLIC_KEY"), ""),
                         json=payment_method_data)
    payment_method_id = resp.json()['data']['id']
    current_app.logger.debug(f"payment_method_id: {payment_method_id}")

    # Attach Payment Method to Intent
    payment_attach_data = {
        "data": {
            "attributes":
                {
                    "payment_method": payment_method_id
                }
        }
    }

    resp = requests.post(f"https://api.paymongo.com/v1/payment_intents/{payment_intent_id}/attach",
                         auth=(current_app.config.get("PAYMONGO_SECRET_KEY"), ""),
                         json=payment_attach_data)

    return resp.json()
