from datetime import datetime as dt

from dateutil.relativedelta import relativedelta

from ..extensions import db


class SubscriptionPlan(db.Model):
    __tablename__ = "subscription_plan"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    subscription_type_id = db.Column(db.Integer,
                                     db.ForeignKey("subscription_type.id", ondelete="CASCADE"),
                                     nullable=False)

    paymongo_transaction = db.relationship('PaymongoPaymentTransaction',
                                           backref='subscription_plan',
                                           cascade='all, delete-orphan',
                                           uselist=False)

    def set_expiration(self, add_months):
        self.expiration = dt.utcnow() + relativedelta(months=add_months)
