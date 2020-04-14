from ..extensions import db


class SubscriptionType(db.Model):
    __tablename__ = "subscription_type"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(25), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    subscription_plans = db.relationship("SubscriptionPlan",
                                         backref="type",
                                         cascade='all, delete-orphan', )

    paymongo_transactions = db.relationship("PaymongoPaymentTransaction",
                                            backref="subscription_type",
                                            cascade='all, delete-orphan', )
