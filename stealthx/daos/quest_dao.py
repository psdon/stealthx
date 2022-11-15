from stealthx.models import Quest
from .base import BaseDAO


class QuestDAO(BaseDAO):
    def new(self, **data):
        obj = self.model(**data)
        self.add_commit_obj(obj)

        return obj


quest_dao = QuestDAO(Quest)
