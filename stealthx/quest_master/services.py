from werkzeug.utils import secure_filename

from stealthx.daos import quest_book_dao, quest_chapter_dao, quest_chapter_vault_dao
from .utils import clean_blob, s3_upload_image


def create_quest_book_service(form):
    """
    create
    :param form:
    :return Quest Book Object:
    """

    avatar_url = s3_upload_image(form.avatar_hidden)

    code = clean_blob(form.quest_title.data) if not form.quest_code.data else form.quest_code.data
    quest_book_data_dao = {
        "title": form.quest_title.data,
        "code": code,
        "short_description": form.short_description.data,
        "long_description": form.long_description.data,
        "avatar_url": avatar_url,
        "avatar_orig_filename": secure_filename(form.avatar_hidden.data.filename),
        "difficulty": form.difficulty.data,
    }
    tags = form.meta_tags_hidden.data.split(",")

    quest_book_obj = quest_book_dao.new(tags, **quest_book_data_dao)

    if quest_book_dao.commit():
        return quest_book_obj  # Success


def save_edited_quest_book_service(quest_book_id, form):
    # TODO: Delete the last saved avatar from s3
    avatar_url = s3_upload_image(form.avatar_hidden) if form.avatar_hidden.data else None
    code = clean_blob(form.quest_title.data) if not form.quest_code.data else form.quest_code.data
    quest_book_data_dao = {
        "title": form.quest_title.data,
        "code": code,
        "short_description": form.short_description.data,
        "long_description": form.long_description.data,
        "avatar_url": avatar_url,
        "avatar_orig_filename": secure_filename(form.avatar_hidden.data.filename) if form.avatar_hidden.data else None,
        "difficulty": form.difficulty.data,
    }
    tags = form.meta_tags_hidden.data.split(",")

    # clean data
    quest_book_data_dao = {k: v for k, v in quest_book_data_dao.items() if v is not None}

    quest_book_obj = quest_book_dao.edit(quest_book_id=quest_book_id, tags=tags, **quest_book_data_dao)

    if quest_book_dao.commit():
        return quest_book_obj  # Success


def create_quest_chapter_service(quest_book_id, chapter_num, form):
    quest_chapter_data = {
        "num": chapter_num,
        "title": form.chapter_title.data,
        "description": form.description_hidden.data,
        "video_url": None,
        "video_orig_filename": secure_filename(form.video_hidden.data.filename) if form.video_hidden.data else None
    }

    # clean data
    quest_chapter_data = {k: v for k, v in quest_chapter_data.items() if v is not None}

    quests_data = []
    for quest in form.quests:
        quests_data.append(quest.data)

    quest_chapter_obj = quest_chapter_dao.new(quest_book_id=quest_book_id,
                                              quests_data=quests_data,
                                              **quest_chapter_data)

    if quest_chapter_dao.commit():
        return quest_chapter_obj


def edit_quest_chapter_service(quest_chapter_id, chapter_num, form):
    quest_chapter_data = {
        "num": chapter_num,
        "title": form.chapter_title.data,
        "description": form.description_hidden.data,
        "video_url": None,
        "video_orig_filename": secure_filename(form.video_hidden.data.filename) if form.video_hidden.data else None
    }

    # clean data
    quest_chapter_data = {k: v for k, v in quest_chapter_data.items() if v is not None}

    quests_data = []
    for quest in form.quests:
        quests_data.append(quest.data)

    quest_chapter_obj = quest_chapter_dao.edit(quest_chapter_id,
                                               quests_data,
                                               **quest_chapter_data)

    if quest_chapter_dao.commit():
        return quest_chapter_obj


def delete_quest_chapter_service(quest_chapter_id, quest_book_id):
    quest_chapter_dao.delete(quest_chapter_id)
    quest_chapter_dao.reset_chapter_num(quest_book_id)

    if quest_chapter_dao.commit():
        return True


def create_chapter_vault_service(quest_chapter_id, form):
    vault_data = {
        "video_url": None,
        "video_orig_filename": secure_filename(form.video_hidden.data.filename) if form.video_hidden.data else None,
        "description": form.description_hidden.data,
        "quest_chapter_id": quest_chapter_id
    }

    # clean data
    vault_data = {k: v for k, v in vault_data.items() if v is not None}

    quest_chapter_vault_dao.new(**vault_data)

    if quest_chapter_vault_dao.commit():
        return True


def edit_chapter_vault_service(quest_chapter_id, form):
    vault_data = {
        "video_url": None,
        "video_orig_filename": secure_filename(form.video_hidden.data.filename) if form.video_hidden.data else None,
        "description": form.description_hidden.data,
        "quest_chapter_id": quest_chapter_id
    }

    # clean data
    vault_data = {k: v for k, v in vault_data.items() if v is not None}

    quest_chapter_vault_dao.edit(**vault_data)

    if quest_chapter_vault_dao.commit():
        return True
