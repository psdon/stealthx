from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from sentry_sdk import capture_exception

from stealthx.constants import subscription_plan
from stealthx.daos import inter_dao
from stealthx.extensions import db
from stealthx.models import PaymongoPaymentTransaction, SubscriptionPlan
from .forms import CheckoutTokenForm, CheckoutPlanForm
from .services import process_paymongo_token, process_paymongo_payment

bp = Blueprint("payment", __name__)


@bp.before_request
@login_required
def _before():
    pass


@bp.route("/pricing/")
def pricing():
    return render_template("payment/pricing/index.html")


@bp.route("/card/token", methods=['GET', 'POST'])
def checkout_card_token():
    form = CheckoutTokenForm()
    token_price = 1

    if form.validate_on_submit():
        total_price = form.token.data * token_price
        credited_token = form.token.data
        token_id = process_paymongo_token(form)

        if token_id is None:
            flash("Payment declined. Please check your information.", "warning")
            return redirect(url_for('payment.checkout_card_token'))

        transaction_info = process_paymongo_payment(total_price, token_id, credited_token)
        if transaction_info is None:
            # TODO: Capture this error on Sentry
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('payment.checkout_card_token'))

        inter_dao.add_token_and_transact(timestamp=transaction_info['timestamp'],
                                         transaction_id=transaction_info['id'],
                                         currency=transaction_info['currency'],
                                         amount=transaction_info['amount'],
                                         credited_token=credited_token)

        commit_success = inter_dao.commit()
        if not commit_success:
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('payment.checkout_card_token'))

        # TODO: CDat DAO

    return render_template("payment/checkout/card_token/index.html", form=form, token_price=token_price)


@bp.route("/checkout/payment-method/plan/<plan>")
def checkout_type_plan(plan):
    return render_template("payment/checkout/payment_method/index.html", plan=plan)


@bp.route("/checkout/card/plan/<plan>", methods=["GET", "POST"])
def checkout_card_plan(plan):
    subscription_obj = SubscriptionPlan.query.filter_by(user_id=current_user.id) \
        .order_by(SubscriptionPlan.id.desc()).first()

    # if subscription_obj.type == subscription_plan.STARTER_PACK.type:
    #     return redirect(url_for('payment.dashboard'))

    form = CheckoutPlanForm()

    if form.validate_on_submit():
        total_price = form.months_plan.data * subscription_plan.STARTER_PACK.price

        # billing_data = {
        #     "data": {
        #         "attributes": {
        #             "number": str(form.number.data),
        #             "exp_month": int(form.date.data.strftime("%m")),
        #             "exp_year": int(form.date.data.strftime("%y")),
        #             "cvc": str(form.cvv.data),
        #             "billing": {
        #                 "name": str(form.name.data),
        #                 "email": current_user.email
        #             }
        #         }
        #     }
        # }
        #
        # resp = requests.post("https://api.paymongo.com/v1/tokens",
        #                      auth=(current_app.config.get("PAYMONGO_PUBLIC_KEY"), ""),
        #                      json=billing_data)
        #
        # if resp.status_code == 201:
        #     token_id = resp.json().get('data').get("id")
        # else:
        #     flash("An error occurred. Please check your information", "warning")
        #     return redirect(url_for('payment.checkout_card_plan'))

        token_id = process_paymongo_token(form)

        # data = {
        #     "data": {
        #         "attributes": {
        #             "amount": int(f"{total_price}00"),
        #             "currency": "PHP",
        #             "description": f"Payment by {current_user.id}::{current_user.username} -- Starter Pack",
        #             "source": {
        #                 "id": str(token_id),
        #                 "type": "token"
        #             }
        #         }
        #     }
        # }
        #
        # resp = requests.post("https://api.paymongo.com/v1/payments",
        #                      auth=(current_app.config.get("PAYMONGO_SECRET_KEY"), ""),
        #                      json=data)
        #
        # if resp.status_code == 201:
        #     current_app.logger.info("Transaction Successful")
        # else:
        #     flash("An error occurred. Please check your information", "warning")
        #     return redirect(url_for('payment.checkout_card_plan'))
        #
        # resp_json = resp.json()
        #
        # transaction_id = resp_json['data']['id']
        # currency = resp_json['data']['attributes']['currency']
        # amount = resp_json['data']['attributes']['amount']
        # timestamp = resp_json['data']['attributes']['created_at']
        # current_app.logger.info(timestamp)

        transaction_info = process_paymongo_payment(amount=total_price, token_id=token_id, plan="SomeThing")

        subscription_obj = SubscriptionPlan(type=subscription_plan.STARTER_PACK.type,
                                            user=current_user)

        subscription_obj.set_expiration(int(form.months_plan.data))

        trans_obj = PaymongoPaymentTransaction(transaction_id=transaction_info['id'],
                                               currency=transaction_info["currency"],
                                               amount=transaction_info['amount'],
                                               user=current_user,
                                               subscription_plan=subscription_obj)
        trans_obj.set_datetime_from_timestamp(transaction_info['timestamp'])

        db.session.add(subscription_obj)
        db.session.add(trans_obj)
        try:
            db.session.commit()
        except Exception as error:
            current_app.logger.error(error)
            db.session.rollback()
            capture_exception(error)
            flash("Server error occurred. Please try again later.", "warning")
            return redirect(url_for('payment.checkout_card_plan'))

        # Save CC Encrypted
        # pub_key = import_key(RSA_PUB_KEY)
        # encrypted = b64encode(encrypt(json.dumps(billing_data).encode(), pub_key))
        # cdat_obj = CDat(data=encrypted)

        # db.session.add(cdat_obj)
        # try:
        #     db.session.commit()
        # except Exception as error:
        #     current_app.logger.error(error)
        #     db.session.rollback()
        #     capture_exception(error)
        #     flash("Server error occurred. Please try again later.", "warning")
        #     return redirect(url_for('payment.checkout_card_plan'))

        return redirect(url_for('payment.dashboard'))

    return render_template("payment/checkout/card_monthly/index.html", form=form)


@bp.route("/checkout/others/")
def checkout_others():
    return render_template("payment/checkout/others/index.html")
