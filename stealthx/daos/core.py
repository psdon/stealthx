from .base import BaseDAO
from stealthx.models import Core


class CoreDAO(BaseDAO):
    def init_user_core(self, user_obj=None, user_id=None):

        # Rank ID 1 :: Spool III
        if user_obj:
            obj = self.model(user=user_obj, current_rank_id=1, highest_rank_id=1)
        else:
            obj = self.model(user_id=user_id, current_rank_id=1, highest_rank_id=1)

        self.add_commit_obj(obj)


core_dao = CoreDAO(Core)
