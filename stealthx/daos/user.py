from stealthx.models import  User
from .core import core_dao
from .base import BaseDAO
from .subscription_plan import subscription_plan_dao
import datetime as dt


class UserDAO(BaseDAO):
    def create_user_obj(self, username, email, password):
        return self.model(username=username, email=email, password=password)

    def register_user(self, username, email, password):
        user_obj = self.create_user_obj(username=username, email=email, password=password)
        core_dao.init_user_core(user_obj=user_obj)
        subscription_plan_dao.init_user_free(user_obj=user_obj)

        self.add_commit_obj(user_obj)

    def get_user_by_email_or_404(self, email):
        return self.model.query.filter_by(email=email).first_or_404()

    def set_email_confirmed(self, email):
        user_obj = self.model.query.filter_by(email=email).first()
        user_obj.email_confirmed = True
        user_obj.email_confirmed_at = dt.datetime.utcnow()

    def reset_password(self, email, password):
        """
        :param email:
        :param password:
        :return: True, if user exists
        """
        user_obj = self.model.query.filter_by(email=email).first()
        if user_obj:
            user_obj.set_password(password)
            return True


user_dao = UserDAO(User)
