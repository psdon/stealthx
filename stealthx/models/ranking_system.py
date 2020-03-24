from stealthx.extensions import db


class RankingSystem(db.Model):
    __tablename__ = "ranking_system"

    id = db.Column(db.Integer, primary_key=True)
    rank = db.Column(db.String(24), nullable=False)
    min_hp = db.Column(db.Integer, nullable=False, default=0)

    users_by_current_rank = db.relationship("Core", backref="current_rank", foreign_keys='Core.current_rank_id', cascade='all, delete-orphan')
    users_by_highest_rank = db.relationship("Core", backref="highest_rank", foreign_keys='Core.highest_rank_id',cascade='all, delete-orphan')
