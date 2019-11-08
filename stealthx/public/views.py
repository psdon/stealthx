# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

from flask import Blueprint, flash, redirect, render_template, request, url_for

from stealthx.auth.forms import RegisterForm
from stealthx.models import User
from stealthx.utils import flash_errors

bp = Blueprint("public", __name__, static_folder="../static")


# @blueprint.route("/", methods=["GET", "POST"])
# def home():
#     """Home page."""
#     form = LoginForm(request.form)
#     current_app.logger.info("Hello from the home page!")
#     # Handle logging in
#     if request.method == "POST":
#         if form.validate_on_submit():
#             login_user(form.user)
#             flash("You are logged in.", "success")
#             redirect_url = request.args.get("next") or url_for("user.members")
#             return redirect(redirect_url)
#         else:
#             flash_errors(form)
#     return render_template("public/home.html", form=form)


@bp.route("/")
def home():
    context = {"no_nav": True,
               "footer_args": "bg-brand-blacklight pt-3",
               "with_dashboard": True
               }
    return render_template(
        "public/home/index.html",
        **context
    )


@bp.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)
