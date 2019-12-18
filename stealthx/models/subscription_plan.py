from ..extensions import db


class SubscriptionPlan(db.Model):
    __tablename__ = "subscription_plan"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    type = db.Column(db.String(25), nullable=False)
    expiration = db.Column(db.DateTime, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)

    paymongo_transaction = db.relationship('PaymongoPaymentTransactions',
                                           backref='SubscriptionPlan',
                                           cascade='all, delete-orphan',
                                           uselist=False)
