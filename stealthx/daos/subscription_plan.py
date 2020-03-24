from .base import BaseDAO
from datetime import datetime as dt
from dateutil.relativedelta import relativedelta
from stealthx.models import SubscriptionPlan

class SubscriptionPlanDAO(BaseDAO):
    def init_user_free(self, user_obj=None, user_id=None, expiration=None):
        if not expiration:
            expiration = dt.utcnow() + relativedelta(years=1)

        # SubscriptionType ID 1 = FREE
        if user_obj:
            obj = self.model(user=user_obj, subscription_type_id=1, expiration=expiration)
        else:
            obj = self.model(user_id=user_id, subscription_type_id=1, expiration=expiration)

        self.add_commit_obj(obj)


subscription_plan_dao = SubscriptionPlanDAO(SubscriptionPlan)