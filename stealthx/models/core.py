from stealthx.extensions import db


class Core(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    token = db.Column(db.Integer, nullable=False, default=0)

    current_rank_id = db.Column(db.Integer, db.ForeignKey("ranking_system.id", ondelete='CASCADE'), nullable=False)
    highest_rank_id = db.Column(db.Integer, db.ForeignKey("ranking_system.id", ondelete='CASCADE'), nullable=False)
