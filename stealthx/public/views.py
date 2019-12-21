# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""

from flask import Blueprint, render_template

bp = Blueprint("public", __name__, static_folder="../static")


@bp.route("/")
def home():
    context = {
        "no_nav": True,
        "footer_args": "bg-brand-blacklight pt-3",
        "with_dashboard": True,
    }
    return render_template("public/home/index.html", **context)

