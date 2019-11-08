# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, current_user, logout_user

from stealthx.models import User
from .forms import LoginForm

bp = Blueprint("auth", __name__)


@bp.route("/sign-in/", methods=["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for('account.dashboard'))

    form = LoginForm()
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
            flash("Incorrect username or password")
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
