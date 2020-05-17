from werkzeug.utils import secure_filename

from stealthx.daos import quest_book_dao


def create_quest_book_service(form):
    """
    create
    :param form:
    :return Quest Book ID:
    """
    quest_book_data_dao = {
        "title": form.quest_title.data,
        "short_description": form.short_description.data,
        "long_description": form.long_description.data,
        "avatar_url": "None",
        "avatar_orig_filename": secure_filename(form.avatar_hidden.data.filename),
        "difficulty": form.difficulty.data,
    }
    tags = form.meta_tags_hidden.data.split(",")

    quest_book_obj = quest_book_dao.new(tags, **quest_book_data_dao)

    if quest_book_dao.commit():
        return quest_book_obj.id  # Success


def save_edited_quest_book_service(quest_book_id, form):
    quest_book_data_dao = {
        "title": form.quest_title.data,
        "short_description": form.short_description.data,
        "long_description": form.long_description.data,
        "avatar_url": None,
        "avatar_orig_filename": secure_filename(form.avatar_hidden.data.filename) if form.avatar_hidden.data else None,
        "difficulty": form.difficulty.data,
    }
    tags = form.meta_tags_hidden.data.split(",")

    # clean data
    quest_book_data_dao = {k: v for k, v in quest_book_data_dao.items() if v is not None}

    quest_book_obj = quest_book_dao.edit(quest_book_id=quest_book_id, tags=tags, **quest_book_data_dao)

    if quest_book_dao.commit():
        return quest_book_obj.id  # Success
