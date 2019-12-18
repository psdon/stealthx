from ..extensions import db
from datetime import datetime as dt


class PaymongoPaymentTransactions(db.Model):
    __tablename__ = "paymongo_payment_transactions"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    transaction_id = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(5), nullable=False, default="PHP")
    amount = db.Column(db.Integer, nullable=False)
    date_time = db.Column(db.DateTime, nullable=False)

    subscription_plan_id = db.Column(db.Integer,
                                     db.ForeignKey("subscription_plan.id", ondelete='CASCADE'),
                                     nullable=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id", ondelete='CASCADE'),
                        nullable=False)

    def __init__(self, **kwargs):
        super(PaymongoPaymentTransactions, self).__init__(**kwargs)

    def set_date_from_timestamp(self, epoch):
        self.date_time = dt.utcfromtimestamp(epoch / 1000)
