import threading

from flask import (
    copy_current_request_context,
    current_app,
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user
from flask_mail import Message

from stealthx.extensions import mail

from .tokens import generate_email_token


def create_email_message(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    return msg


def send_async_email(to, subject, template):
    msg = create_email_message(to, subject, template)

    @copy_current_request_context
    def send_message(message):
        mail.send(message)

    sender = threading.Thread(name="mail_sender", target=send_message, args=(msg,))
    sender.start()


def send_confirm_email(email):
    token = generate_email_token(email)
    # TODO: Create Different URL Route for 'First Registration' & Confirming Another Email
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    # TODO: Create Good Looking Email Verification Template
    template = render_template("auth/email/confirm_email.html", confirm_url=confirm_url, user_email=email)
    send_async_email(to=email, subject="Confirm Email", template=template)

    return 0


def send_recover_account_email(email):
    # TODO: Create Good Looking Account Recovery Template
    token = generate_email_token(email, expires_sec=600)
    reset_url = url_for("auth.reset_password", token=token, _external=True)
    template = render_template("auth/email/recover_account.html", reset_url=reset_url)
    send_async_email(to=email, subject="Account Recovery", template=template)


def check_user_status():
    if current_user.is_authenticated:
        # Email should be confirmed
        if not current_user.email_confirmed:
            return redirect(url_for("auth.confirm_your_email"))
