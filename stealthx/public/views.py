# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

from flask import Blueprint, render_template, current_app, redirect, request, json

import hmac
import hashlib
import requests
from stealthx.extensions import csrf_protect

bp = Blueprint("public", __name__, static_folder="../static")


@bp.route("/")
def home():
    context = {
        "no_nav": True,
        "footer_args": "bg-brand-blacklight pt-3",
        "with_dashboard": True,
    }
    return render_template("public/home/index.html", **context)


@bp.route("/test")
def test():

    url = "https://api.paymongo.com/v1/sources"

    payload = {"data":
                   {"attributes":
                        {"type": "gcash",
                         "amount": 10000,
                         "currency": "PHP",
                         "redirect": {"success": "https://test.com/success",
                                      "failed": "https://test.com/failed"
                                      }
                         }
                    }
               }

    resp = requests.post(url, json=payload, auth=(current_app.config.get("PAYMONGO_PUBLIC_KEY"), ""),)

    redir_url = resp.json().get('data').get("attributes").get("redirect").get('checkout_url')

    return redirect(redir_url)


@bp.route("/webhook")
def webhook():
    webhook_payload = {"data": {
        "attributes": {
            "url": "http://e7835098.ngrok.io/test1",
            "events": ["source.chargeable"]
        }
    }}
    resp = requests.post("https://api.paymongo.com/v1/webhooks",
                         json=webhook_payload,
                         auth=(current_app.config.get("PAYMONGO_SECRET_KEY"), ""), )
    return resp.text


@bp.route("/test1", methods=['POST'])
@csrf_protect.exempt
def gcash_hook():
    if request.headers.get('Content-Type') != "application/json":
        return ""

    if request.headers.get('Paymongo-Signature') is None:
        return ""

    signature = request.headers.get('Paymongo-Signature')
    # current_app.logger.info(signature)

    timestamp, test_mode, live_mode = signature.split(",")
    resp_json = request.json

    webhook_secret_key = 'whsk_oWH59BhvGAyMBciFJPtK3aJb'

    # check_sig = f"{timestamp[2:]}.{json.dumps(resp_json)}"
    # current_app.logger.info(check_sig)
    #
    # check_sig = hmac.new(bytes(webhook_secret_key, 'latin-1'), msg=bytes(check_sig, 'latin-1'),
    #                      digestmod=hashlib.sha256).hexdigest().lower()
    # current_app.logger.info(check_sig)


    # current_app.logger.info(result)

    trans_id = resp_json.get('data').get("attributes").get("data").get("id")
    trans_amount = resp_json.get('data').get("attributes").get("data").get("attributes").get("amount")
    trans_status = resp_json.get('data').get("attributes").get("data").get("attributes").get("status")
    trans_type = resp_json.get('data').get("attributes").get("data").get("attributes").get("type")

    if trans_status != "chargeable" or trans_type != "gcash":
        current_app.logger.info("Failed @ chargeable or gcash")
        return ""

    payment_payload = {"data": {
        "attributes": {
            "amount": trans_amount,
            "currency": "PHP",
            "source": {
                "id": trans_id,
                "type": "source"
            }
        }
    }}

    resp = requests.post("https://api.paymongo.com/v1/payments",
                         auth=(current_app.config.get("PAYMONGO_SECRET_KEY"), ""),
                         json=payment_payload)

    current_app.logger.info(resp.text)

    return ""
