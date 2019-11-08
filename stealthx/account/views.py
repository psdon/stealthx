from flask import Blueprint, render_template
from flask_login import login_required

bp = Blueprint("account", __name__, url_prefix="/account")


@bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("account/dashboard/index.html")
