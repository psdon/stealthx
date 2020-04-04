from flask_login import current_user

from stealthx.models import SubscriptionPlan, SubscriptionType
from .base import BaseDAO


class SubscriptionPlanDAO(BaseDAO):
    def init_user_free(self, user_obj=None, user_id=None):

        # SubscriptionType ID 1 = FREE
        if user_obj:
            obj = self.model(user=user_obj, subscription_type_id=1)
        else:
            obj = self.model(user_id=user_id, subscription_type_id=1)

        self.add_commit_obj(obj)

    @staticmethod
    def subscribe(plan, duration_months):
        """
        :param plan: Subscription Plan Name
        :param duration_months:
        :return:
        """
        plan_id = SubscriptionType.query.filter_by(name=plan).first().id

        current_user.subscription.subscription_type_id = plan_id
        current_user.subscription.set_expiration(duration_months)

        return plan_id


subscription_plan_dao = SubscriptionPlanDAO(SubscriptionPlan)
