from flask import Blueprint, render_template
from stealthx.library.helper import auth_required
from stealthx.watchers.watcher import register_watchers

bp = Blueprint("quest_master", __name__, static_folder="../static", url_prefix="/quest-master")


@bp.before_request
@auth_required
def _before():
    pass


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/create")
def create_quest():
    return render_template("quest_master/create_quest/index.html")
