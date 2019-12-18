from flask import Blueprint, render_template, current_app, redirect, url_for, flash
from flask_login import login_required, current_user
import requests

from stealthx.watcher import register_watchers
from .forms import CheckoutForm
from stealthx.constants import SubscriptionPlans

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/dashboard/")
@login_required
def dashboard():
    return render_template("account/dashboard/index.html")


@bp.route("/pricing/")
@login_required
def pricing():
    return render_template("account/pricing/index.html")


@bp.route("/checkout/", methods=["GET", "POST"])
@login_required
def checkout():
    form = CheckoutForm()
    plan = SubscriptionPlans()

    if form.validate_on_submit():
        total = form.months_plan.data * plan.STARTER_PACK

        data = {
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
                             json=data)

        if resp.status_code == 201:
            token = resp.json().get('data').get("id")
        else:
            flash("An error occurred. Please check your information", "warning")
            return redirect(url_for('account.checkout'))

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
            # Save transaction ID
            # Save CC Information and Encrypted
        else:
            flash("An error occurred. Please check your information", "warning")
            return redirect(url_for('account.checkout'))

        return redirect(url_for('account.checkout'))

    return render_template("account/checkout/index.html", form=form)
