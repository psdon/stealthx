from flask import Blueprint, render_template
from stealthx.library.helper import auth_required


bp = Blueprint("journey", __name__)


@bp.before_request
@auth_required
def _before():
    pass


@bp.route("/your-journey")
def your_journey():
    return render_template("journey/your_journey/index.html")
