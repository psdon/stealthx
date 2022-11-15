from stealthx.models import QuestChapterVault
from .base import BaseDAO
from .quest_dao import quest_dao


class QuestChapterVaultDAO(BaseDAO):
    def new(self, **kwargs):
        obj = self.model(**kwargs)
        self.add_commit_obj(obj)

        return obj

    def edit(self,quest_chapter_id, **kwargs):
        obj = self.model.query.filter_by(quest_chapter_id=quest_chapter_id).first()

        for key, value in kwargs.items():
            setattr(obj, key, value)

        return obj


quest_chapter_vault_dao = QuestChapterVaultDAO(QuestChapterVault)