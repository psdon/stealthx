from flask_login import current_user

from stealthx.models import PaymongoPaymentTransaction
from .base import BaseDAO


class PaymongoPTDAO(BaseDAO):
    def new(self, timestamp, **kwargs):
        """
        Create new transaction
        :param timestamp:
        :param kwargs:
            - transaction_id
            - currency
            - amount
            - subscription_id
            - user: default current_user
        :return:
        """
        obj = self.model(user=current_user, **kwargs)
        obj.set_datetime_from_timestamp(timestamp)


paymongo_pt_dao = PaymongoPTDAO(PaymongoPaymentTransaction)
