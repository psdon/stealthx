from flask_login import current_user

from stealthx.models import Core
from .base import BaseDAO


class CoreDAO(BaseDAO):
    def init_user_core(self, user_obj=None, user_id=None):

        # Rank ID 1 :: Spool III
        if user_obj:
            obj = self.model(user=user_obj, current_rank_id=1, highest_rank_id=1)
        else:
            obj = self.model(user_id=user_id, current_rank_id=1, highest_rank_id=1)

        self.add_commit_obj(obj)

    @staticmethod
    def add_token(credited_token):
        current_user.core.token += credited_token


core_dao = CoreDAO(Core)
