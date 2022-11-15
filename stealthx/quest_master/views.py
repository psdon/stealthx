from flask import Blueprint, render_template, redirect, url_for, flash, abort, request, current_app
from flask_login import current_user

from stealthx.library.helper import auth_required
from stealthx.models import QuestBook
from stealthx.watchers.watcher import register_watchers
from .forms import QuestBookForm, QuestChapterForm, QuestChapterVaultForm
from .services import create_quest_book_service, save_edited_quest_book_service, create_quest_chapter_service, \
    edit_quest_chapter_service, delete_quest_chapter_service, create_chapter_vault_service, edit_chapter_vault_service

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
        quest_book_obj = create_quest_book_service(form)
        if quest_book_obj:
            flash("You have saved it successfully", "success")
            return redirect(url_for('quest_master.edit_quest_book', quest_book_code=quest_book_obj.code))

        flash("An error occurred. Please try again later", "warning")

    return render_template("quest_master/quest_book/index.html", form=form, sb_create_quest=True
                           )


@bp.route("/book/<string:quest_book_code>/edit", methods=['GET', 'POST'])
def edit_quest_book(quest_book_code):
    quest_book_obj = QuestBook.query.filter_by(code=quest_book_code, quest_master_user_id=current_user.id).first()

    if not quest_book_obj:
        return abort(404)

    chapters_obj = quest_book_obj.chapters.all()

    data = {
        "sb_manage_quests": True,
        "title": "Edit Quest",
        'avatar_orig_filename': quest_book_obj.avatar_orig_filename,
        "quest_book_code": quest_book_code,
        "chapters_obj": chapters_obj,
    }

    form = QuestBookForm(quest_book_obj=quest_book_obj)
    if form.validate_on_submit():
        quest_book_obj = save_edited_quest_book_service(quest_book_obj.id, form)

        if quest_book_obj:
            flash("You have saved it successfully", "success")
            return redirect(url_for('quest_master.edit_quest_book', quest_book_code=quest_book_obj.code))

        flash("An error occurred. Please try again later", "warning")

    if not form.errors:
        form.quest_title.data = quest_book_obj.title
        form.short_description.data = quest_book_obj.short_description
        form.long_description.data = quest_book_obj.long_description
        form.difficulty.data = quest_book_obj.difficulty
        form.quest_code.data = quest_book_obj.code

        tags = []
        for tag_obj in quest_book_obj.tags:
            tags.append(tag_obj.name)

        form.meta_tags_hidden.data = ",".join(tags)

    return render_template("quest_master/quest_book/index.html", form=form, **data)


@bp.route("/quest-material", methods=['GET', 'POST'])
def quest_material():
    return render_template("quest_master/quest_material/index.html")


@bp.route("/book/<string:quest_book_code>/create-chapter", methods=['GET', 'POST'])
def create_quest_chapter(quest_book_code):
    quest_book_obj = QuestBook.query.filter_by(code=quest_book_code, quest_master_user_id=current_user.id).first()

    if not quest_book_obj:
        return abort(404)

    chapters_obj = quest_book_obj.chapters.all()
    chapter_num = len(chapters_obj) + 1

    data = {
        "sb_manage_quests": True,
        "upload_by_file": url_for('quest_master.editor_js_upload_by_file'),
        "upload_by_url": url_for('quest_master.editor_js_upload_by_file'),
        "chapter_num": chapter_num,
        "quest_book_code": quest_book_code
    }
    form = QuestChapterForm()

    if form.validate_on_submit():
        quest_chapter_obj = create_quest_chapter_service(quest_book_obj.id, chapter_num, form)

        if quest_chapter_obj:
            flash("You have saved it successfully", "success")

            return redirect(url_for('quest_master.edit_quest_chapter',
                                    quest_book_code=quest_book_code,
                                    quest_chapter_num=quest_chapter_obj.num))

        flash("An error occurred. Please try again later", "warning")

    return render_template("quest_master/quest_chapter/index.html", form=form, **data)


@bp.route("/editor-js/upload-by-file", methods=['GET', 'POST'])
def editor_js_upload_by_file():
    current_app.logger.info(request.files)

    return {"success": 1,
            "file": {
                "url": "https://www.tesla.com/tesla_theme/assets/img/_vehicle_redesign/roadster_and_semi/roadster/hero.jpg"
            }
            }


@bp.route("/book/<string:quest_book_code>/chapter/<string:quest_chapter_num>/edit", methods=['GET', 'POST'])
def edit_quest_chapter(quest_book_code, quest_chapter_num):
    quest_book_obj = QuestBook.query.filter_by(code=quest_book_code, quest_master_user_id=current_user.id).first()

    if not quest_book_obj:
        return abort(404)

    quest_chapter_obj = quest_book_obj.chapters.filter_by(num=quest_chapter_num).first()

    if not quest_chapter_obj:
        return redirect(url_for('quest_master.edit_quest_book', quest_book_code=quest_book_code))

    form = QuestChapterForm()

    if form.validate_on_submit():
        quest_chapter_obj = edit_quest_chapter_service(quest_chapter_id=quest_chapter_obj.id,
                                                       chapter_num=quest_chapter_obj.num,
                                                       form=form)

        if quest_chapter_obj:
            flash("You have saved it successfully", "success")
            return redirect(url_for('quest_master.edit_quest_chapter',
                                    quest_book_code=quest_book_code,
                                    quest_chapter_num=quest_chapter_num))

        flash("An error occurred. Please try again later", "warning")

    if not form.errors:
        form.chapter_title.data = quest_chapter_obj.title
        form.description_hidden.data = quest_chapter_obj.description

        for index, quest in enumerate(quest_chapter_obj.quests):
            data = {
                "quest": quest.quest,
                "answer": quest.answer
            }

            if index == 0:
                form.quests[0].quest.data = quest.quest
                form.quests[0].answer.data = quest.answer
                continue

            form.quests.append_entry(data)

    data = {
        "sb_manage_quests": True,
        "upload_by_file": url_for('quest_master.editor_js_upload_by_file'),
        "upload_by_url": url_for('quest_master.editor_js_upload_by_file'),
        "video_orig_filename": quest_chapter_obj.video_orig_filename if quest_chapter_obj.video_orig_filename else "",
        "title": "Edit Chapter",
        "chapter_num": quest_chapter_num,
        "book_code": quest_book_code,
        "quest_chapter_obj": quest_chapter_obj
    }

    return render_template("quest_master/quest_chapter/index.html", form=form, **data)


@bp.route("/book/<string:quest_book_code>/delete/<string:quest_chapter_num>", methods=['GET'])
def delete_quest_chapter(quest_book_code, quest_chapter_num):
    quest_book_obj = QuestBook.query.filter_by(code=quest_book_code, quest_master_user_id=current_user.id).first()

    if not quest_book_obj:
        return abort(404)

    if request.referrer != url_for('quest_master.edit_quest_book', quest_book_code=quest_book_code, _external=True):
        return abort(404)

    quest_chapter_obj = quest_book_obj.chapters.filter_by(num=quest_chapter_num).first()

    if not quest_chapter_obj:
        return redirect(url_for('quest_master.edit_quest_book', quest_book_code=quest_book_code))

    if not delete_quest_chapter_service(quest_chapter_obj.id, quest_book_obj.id):
        flash("An error occurred. Please try again later", "warning")

    return redirect(url_for('quest_master.edit_quest_book', quest_book_code=quest_book_code))


@bp.route("/book/<string:quest_book_code>/chapter/<string:quest_chapter_num>/create-vault", methods=['GET', 'POST'])
def create_quest_chapter_vault(quest_book_code, quest_chapter_num):
    quest_book_obj = QuestBook.query.filter_by(code=quest_book_code, quest_master_user_id=current_user.id).first()

    if not quest_book_obj:
        return abort(404)

    quest_chapter_obj = quest_book_obj.chapters.filter_by(num=quest_chapter_num).first()

    if not quest_chapter_obj:
        return redirect(url_for('quest_master.edit_quest_book', quest_book_code=quest_book_code))

    if quest_chapter_obj.vault:
        return redirect(url_for('quest_master.edit_quest_chapter_vault', quest_book_code=quest_book_code,
                                quest_chapter_num=quest_chapter_num))

    form = QuestChapterVaultForm()
    if form.validate_on_submit():
        if create_chapter_vault_service(quest_chapter_obj.id, form):
            flash("You have saved it successfully", "success")
            return redirect(url_for('quest_master.create_quest_chapter_vault',
                                    quest_book_code=quest_book_code,
                                    quest_chapter_num=quest_chapter_num))

        flash("An error occurred. Please try again later", "warning")

    data = {
        "chapter_num": quest_chapter_obj.num,
        "chapter_title": quest_chapter_obj.title,
        "book_code": quest_book_code,
        "sb_manage_quests": True,
        "upload_by_file": url_for('quest_master.editor_js_upload_by_file'),
        "upload_by_url": url_for('quest_master.editor_js_upload_by_file'),
        "video_orig_filename": quest_chapter_obj.video_orig_filename if quest_chapter_obj.video_orig_filename else "",
        "title": "Create Vault",
    }

    return render_template("quest_master/quest_chapter_vault/index.html", form=form, **data)


@bp.route("/book/<string:quest_book_code>/chapter/<string:quest_chapter_num>/edit-vault", methods=['GET', 'POST'])
def edit_quest_chapter_vault(quest_book_code, quest_chapter_num):
    quest_book_obj = QuestBook.query.filter_by(code=quest_book_code, quest_master_user_id=current_user.id).first()

    if not quest_book_obj:
        return abort(404)

    quest_chapter_obj = quest_book_obj.chapters.filter_by(num=quest_chapter_num).first()

    if not quest_chapter_obj:
        return redirect(url_for('quest_master.edit_quest_book', quest_book_code=quest_book_code))

    vault_obj = quest_chapter_obj.vault

    form = QuestChapterVaultForm()
    if form.validate_on_submit():
        if edit_chapter_vault_service(quest_chapter_obj.id, form):
            flash("You have saved it successfully", "success")
            return redirect(url_for('quest_master.create_quest_chapter_vault',
                                    quest_book_code=quest_book_code,
                                    quest_chapter_num=quest_chapter_num))

        flash("An error occurred. Please try again later", "warning")

    data = {
        "chapter_num": quest_chapter_obj.num,
        "chapter_title": quest_chapter_obj.title,
        "book_code": quest_book_code,
        "sb_manage_quests": True,
        "upload_by_file": url_for('quest_master.editor_js_upload_by_file'),
        "upload_by_url": url_for('quest_master.editor_js_upload_by_file'),
        "title": "Edit Vault",
        "video_orig_filename": vault_obj.video_orig_filename if vault_obj.video_orig_filename else ""
    }

    if not form.errors:
        form.description_hidden.data = vault_obj.description

    return render_template("quest_master/quest_chapter_vault/index.html", form=form, **data)