# Business Logic

import requests
from flask import current_app
from flask_login import current_user


def process_paymongo_token(form):
    """
    Process Token Object, aka. payment source

    :param form:
        - number: Credit Card number
        - exp_month
        - exp_year
        - cvc
        - billing:
            - name
            - email

    :return: Token ID
    :return: None, if failed
    """
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

    if resp.status_code == 200:
        return resp.json().get('data')["id"]


def process_paymongo_payment(amount, token_id, plan=None):
    """
    Process Paymongo payment
    :param amount:
    :param token_id:
    :param credited_token:
    :param plan:
    :return: Dict, if success
    """

    data = {
        "data": {
            "attributes": {
                "amount": int(f"{amount}00"),
                "currency": "PHP",
                "description": f"Payment by {current_user.id}::{current_user.username} -- {plan}",
                "source": {
                    "id": str(token_id),
                    "type": "token"
                }
            }
        }
    }

    resp = requests.post("https://api.paymongo.com/v1/payments",
                         auth=(current_app.config.get("PAYMONGO_SECRET_KEY"), ""),
                         json=data)

    if resp.status_code == 200:
        resp_json = resp.json()

        return {
            "id": resp_json['data']['id'],
            "currency": resp_json['data']['attributes']['currency'],
            "amount": resp_json['data']['attributes']['amount'],
            "timestamp": resp_json['data']['attributes']['created_at']
        }


def process_paymongo_payment_method(form):
    pass