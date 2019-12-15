from flask import Blueprint, render_template
from flask_login import login_required

from stealthx.watcher import register_watchers

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/dashboard/")
@login_required
def dashboard():
    return render_template("account/dashboard/index.html")


@bp.route("/pricing/")
@login_required
def pricing():
    return render_template("account/pricing/index.html")