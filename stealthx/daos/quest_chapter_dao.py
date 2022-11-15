from flask_login import current_user

from stealthx.models import QuestChapter
from .base import BaseDAO
from .quest_dao import quest_dao


class QuestChapterDAO(BaseDAO):
    def new(self, quest_book_id, quests_data, **kwargs):
        obj = self.model(quest_book_id=quest_book_id, **kwargs)
        self.add_commit_obj(obj)

        for quest in quests_data:
            obj.quests.append(quest_dao.new(**quest))

        return obj

    def edit(self, quest_chapter_id, quests_data, **kwargs):
        obj = self.model.query.get(quest_chapter_id)

        if obj.quest_book.quest_master_user_id != current_user.id:
            return None

        for key, value in kwargs.items():
            setattr(obj, key, value)

        # Delete All Quests
        for quest in obj.quests:
            self.delete_obj(quest)

        for quest in quests_data:
            obj.quests.append(quest_dao.new(**quest))

        return obj

    def delete(self, quest_chapter_id):
        obj = self.model.query.get(quest_chapter_id)

        if obj.quest_book.quest_master_user_id != current_user.id:
            return None

        self.delete_obj(obj)

        return obj

    def reset_chapter_num(self, quest_book_id):
        objs = self.model.query.filter_by(quest_book_id=quest_book_id).all()

        for index, obj in enumerate(objs):
            obj.num = index + 1


quest_chapter_dao = QuestChapterDAO(QuestChapter)
