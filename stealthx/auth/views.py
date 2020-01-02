# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, request, url_for, current_app
from flask_login import current_user, login_required, login_user, logout_user
from sentry_sdk import capture_exception
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta

from stealthx.extensions import db
from stealthx.models import User, SubscriptionPlan
from stealthx.constants import subscription_plan

from .forms import RecoverForm, ResetPasswordForm, SignInForm, SignUpForm, ChangeEmailForm
from .tokens import verify_email_token
from .utils import send_confirm_email, send_recover_account_email

bp = Blueprint("auth", __name__)


@bp.route("/sign-in/", methods=["GET", "POST"])
def sign_in():
    # TODO: Limit 10 wrong password attempt per account, unless Reset Password Initiated
    # TODO: Limit to 20 wrong password attempt per IP. Blocked that IP for a day. Also track by Cookies.

    if current_user.is_authenticated:
        return redirect(url_for("account.dashboard"))

    form = SignInForm()
    context = {"form": form, "logo_only": True}

    if form.validate_on_submit():
        user = form.username_or_email.data
        password = form.password.data
        user_obj = User.query.filter(
            (User.email == user) | (User.username == user)
        ).first()

        if user_obj and user_obj.check_password(password):
            login_user(user_obj)

        else:
            flash("Incorrect username or password", "warning")
            return render_template("auth/sign_in/index.html", **context)

        safe_redirect = None
        if request.args.get("next"):
            safe_redirect = f"{request.host_url}{request.args.get('next').strip('/')}"

        return redirect(safe_redirect or url_for("account.dashboard"))
    return render_template("auth/sign_in/index.html", **context)


@bp.route("/sign-out/")
def sign_out():
    """Logout."""
    logout_user()
    return redirect(url_for("public.home"))


@bp.route("/sign-up/", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("account.dashboard"))

    form = SignUpForm()
    if form.validate_on_submit():

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        expiration = dt.utcnow() + relativedelta(years=1)

        user_subscription = SubscriptionPlan(user=new_user, type=subscription_plan.FREE.type, expiration=expiration)

        db.session.add(new_user)
        db.session.add(user_subscription)
        try:
            db.session.commit()
            send_confirm_email(new_user.email)
            flash("You have signed up successfully. Please check your email", "success")
            return redirect(url_for("auth.sign_in"))
        except Exception as error:
            db.session.rollback()
            capture_exception(error)
            flash("Oops, an error occurred. Please try again later.", "warning")

    return render_template("auth/sign_up/index.html", form=form)


@bp.route("/confirm-your-email", methods=["GET", "POST"])
@login_required
def confirm_your_email():
    """
    Display if user email is not confirmed.
    """

    if current_user.email_confirmed:
        return redirect(url_for("account.dashboard"))

    form = ChangeEmailForm()

    if form.validate_on_submit():
        user = User.query.get(current_user.id)
        user.email = form.email.data

        try:
            db.session.commit()
            send_confirm_email(form.email.data)
        except Exception as error:
            db.session.rollback()
            capture_exception(error)
            flash("Oops, an error occurred. Please try again later.", "warning")
    else:
        form.email.data = current_user.email

    return render_template("auth/email/confirm_your_email.html", form=form)


@bp.route("/resend-confirm-email")
@login_required
def resend_confirm_email():
    if current_user.email_confirmed:
        return redirect(url_for("account.dashboard"))

    send_confirm_email(current_user.email)
    return redirect(url_for('auth.confirm_your_email'))


@bp.route("/confirm/<token>")
def confirm_email(token):
    if current_user.is_authenticated:
        logout_user()

    email = verify_email_token(token)
    if email is None:
        flash("The confirmation link is invalid or has expired.", "warning")
        return redirect(url_for("auth.sign_in"))
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash("Email already confirmed. Please sign in.", "success")
    else:
        user.set_email_confirmed()
        try:
            db.session.commit()
            flash(
                "You have successfully confirmed your email. You can now sign in.",
                "success",
            )
        except Exception as error:
            db.session.rollback()
            capture_exception(error)
            flash("Oops, an error occurred. Please try again later.", "warning")

    return redirect(url_for("auth.sign_in"))


@bp.route("/recover/", methods=["GET", "POST"])
def account_recover():
    """
    Find the user account and send recovery email
    """
    # TODO: Limit to 5 email sent in 6 hours.
    if current_user.is_authenticated:
        return redirect(url_for("account.dashboard"))

    form = RecoverForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_recover_account_email(email=user.email)
        flash("We have sent you an email. Please check your email inbox.", "success")
    return render_template("auth/recover/find_account.html", form=form)


@bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    """
    Reset Password page.
    """
    # TODO: One time reset link.
    # TODO: Limit 3 reset password per day

    email = verify_email_token(token)
    if email is None:
        flash("The reset password link is invalid or has expired.", "warning")
        return redirect(url_for("auth.account_recover"))

    if current_user.is_authenticated:
        logout_user()

    form = ResetPasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=email).first()

        if user:
            user.set_password(form.password.data)
            try:
                db.session.commit()
                flash(
                    "You have successfully reset your password. You can now sign in.",
                    "success",
                )
                return redirect(url_for("auth.sign_in"))
            except Exception as error:
                db.session.rollback()
                capture_exception(error)
                flash("Oops, an error occurred. Please try again later.", "warning")
        else:
            flash("Oops, an error occurred. Please try again later.", "warning")

    return render_template("auth/recover/reset_password.html", form=form)
