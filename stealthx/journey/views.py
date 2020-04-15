from flask import Blueprint, render_template

from stealthx.library.helper import auth_required
from stealthx.watchers.watcher import register_watchers

bp = Blueprint("journey", __name__)


@bp.before_request
@auth_required
def _before():
    pass


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/your-journey")
def your_journey():
    return render_template("journey/your_journey/index.html")
