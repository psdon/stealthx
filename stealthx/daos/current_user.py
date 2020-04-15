# Database Access Objects

from flask_login import current_user

from .base import BaseDAO


class CurrentUserDAO(BaseDAO):
    def change_username(self, username):
        self.model.username = username

    def change_email(self, email, set_confirm=True):
        self.model.email = email

        if set_confirm:
            self.model.email_confirmed = False

    def change_password(self, password):
        self.model.set_password(password)

    def set_session_token(self, token):
        self.model.session_token = token

    def set_subscription_free(self):
        self.model.subscription.expiration = None
        # free
        self.model.subscription.subscription_type_id = 1


current_user_dao = CurrentUserDAO(current_user)
