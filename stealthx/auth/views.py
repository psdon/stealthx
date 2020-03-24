# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from stealthx.models import User
from .forms import RecoverForm, ResetPasswordForm, SignInForm, SignUpForm, ChangeEmailForm
from .services import sign_up_service, confirm_your_email_service, confirm_email_service, reset_password_service
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
        success_flag = sign_up_service(username=form.username.data,
                                       email=form.email.data,
                                       password=form.password.data)

        if success_flag:
            return redirect(url_for("auth.sign_in"))

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
        confirm_your_email_service(email=form.email.data)
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

    confirm_email_service(email=email)

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
        service_success = reset_password_service(email, password=form.password.data)

        if service_success:
            return redirect(url_for("auth.sign_in"))
    return render_template("auth/recover/reset_password.html", form=form)
