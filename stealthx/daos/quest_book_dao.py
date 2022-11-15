from flask_login import current_user

from stealthx.models import QuestBook
from .base import BaseDAO
from .tags_dao import tags_dao


class QuestBookDAO(BaseDAO):
    def new(self, tags, **kwargs):
        """
        Create new Quest Book, and append tags
        :param tags: Meta Tags
        :param kwargs: Quest Book Model fields
        :return True: if Success
        """
        obj = self.model(quest_master_user_id=current_user.id, **kwargs)

        for tag in tags:
            tag_obj = tags_dao.new(tag)
            obj.tags.append(tag_obj)

        self.add_commit_obj(obj)

        return obj

    def edit(self, quest_book_id, tags, **kwargs):
        obj = self.model.query.filter_by(quest_master_user_id=current_user.id, id=quest_book_id).first()

        for key, value in kwargs.items():
            setattr(obj, key, value)

        obj.tags = []
        self.commit()

        for tag in tags:
            tag_obj = tags_dao.new(tag)
            obj.tags.append(tag_obj)

        return obj


quest_book_dao = QuestBookDAO(QuestBook)
