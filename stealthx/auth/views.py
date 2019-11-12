# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user, login_required

from stealthx.models import User
from stealthx.extensions import db
from .forms import SignInForm, SignUpForm
from .utils import send_confirm_email
from .tokens import verify_email_token

bp = Blueprint("auth", __name__)


@bp.route("/sign-in/", methods=["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('account.dashboard'))

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


@bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for('account.dashboard'))

    form = SignUpForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)

        db.session.add(new_user)
        try:
            db.session.commit()
            send_confirm_email(new_user.email)
            flash("You have signed up successfully. Please check your email", "success")
            return redirect(url_for('auth.sign_in'))
        except Exception:
            db.session.rollback()
            flash("Oops, an error occurred. Please try again later.", "warning")

    return render_template("auth/sign_up/index.html", form=form)


@bp.route("/confirm-your-email")
@login_required
def confirm_your_email():
    """
    Display if user email is not confirmed.
    """
    if current_user.email_confirmed:
        return redirect(url_for("account.dashboard"))

    return render_template("auth/email/confirm_your_email.html")


@bp.route("/resend-confirm-email")
@login_required
def resend_confirm_email():
    if current_user.email_confirmed:
        return redirect(url_for("account.dashboard"))

    send_confirm_email(current_user.email)
    return render_template("auth/email/confirm_your_email.html", )


@bp.route('/confirm/<token>')
def confirm_email(token):
    if current_user.is_authenticated:
        logout_user()

    email = verify_email_token(token)
    if email is None:
        flash('The confirmation link is invalid or has expired.', 'warning')
        return redirect(url_for('auth.sign_in'))
    user = User.query.filter_by(email=email).first_or_404()
    if user.email_confirmed:
        flash('Email already confirmed. Please sign in.', 'success')
    else:
        user.email_confirmed = True
        try:
            db.session.commit()
            flash('You have successfully confirmed your email. You can now sign in!', 'success')
        except Exception:
            db.session.rollback()
            flash("Oops, an error occurred. Please try again later.", "warning")

    return redirect(url_for('auth.sign_in'))
