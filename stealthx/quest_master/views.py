from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user

from stealthx.library.helper import auth_required
from stealthx.models import QuestBook
from stealthx.watchers.watcher import register_watchers
from .forms import QuestBookForm
from .services import create_quest_book_service, save_edited_quest_book_service

bp = Blueprint("quest_master", __name__, static_folder="../static", url_prefix="/quest-master")


@bp.before_request
@auth_required
def _before():
    pass


@bp.after_request
def _(response):
    return register_watchers(response)


@bp.route("/create", methods=['GET', 'POST'])
def create_quest_book():
    form = QuestBookForm()

    if form.validate_on_submit():
        quest_book_id = create_quest_book_service(form)
        if quest_book_id:
            flash("You have saved it successfully", "success")
            return redirect(url_for('quest_master.edit_quest_book', quest_book_id=quest_book_id))

        flash("An error occurred. Please try again later", "warning")

    return render_template("quest_master/quest_book/index.html", form=form, sb_create_quest=True
                           )


@bp.route("/edit/<int:quest_book_id>", methods=['GET', 'POST'])
def edit_quest_book(quest_book_id):
    quest_book_obj = QuestBook.query.filter_by(id=quest_book_id, quest_master_user_id=current_user.id).first()

    if not quest_book_obj:
        return redirect(url_for('quest_master.create_quest_book'))

    data = {
        "sb_manage_quests": True,
        "title": "Edit Quest",
        'avatar_orig_filename': quest_book_obj.avatar_orig_filename,
    }

    form = QuestBookForm(quest_book_obj=quest_book_obj)
    if form.validate_on_submit():
        if save_edited_quest_book_service(quest_book_obj.id, form):
            flash("You have saved it successfully", "success")
            return redirect(url_for('quest_master.edit_quest_book', quest_book_id=quest_book_id))

        flash("An error occurred. Please try again later", "warning")
    else:
        form.quest_title.data = quest_book_obj.title
        form.short_description.data = quest_book_obj.short_description
        form.long_description.data = quest_book_obj.long_description
        form.difficulty.data = quest_book_obj.difficulty

        tags = []
        for tag_obj in quest_book_obj.tags:
            tags.append(tag_obj.name)

        form.meta_tags_hidden.data = ",".join(tags)
    return render_template("quest_master/quest_book/index.html", form=form, **data)


@bp.route("/quest-material", methods=['GET', 'POST'])
def quest_material():
    return render_template("quest_master/quest_material/index.html")
