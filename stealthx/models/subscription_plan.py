from datetime import datetime as dt

from dateutil.relativedelta import relativedelta

from ..extensions import db


class SubscriptionPlan(db.Model):
    __tablename__ = "subscription_plan"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    expiration = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    subscription_type_id = db.Column(db.Integer,
                                     db.ForeignKey("subscription_type.id", ondelete="CASCADE"),
                                     nullable=False)

    def set_expiration(self, add_months, based_date=None):
        if based_date is None:
            self.expiration = dt.utcnow() + relativedelta(months=add_months)
        else:
            self.expiration = self.expiration + relativedelta(months=add_months)