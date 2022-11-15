from ..extensions import db


class Quest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quest = db.Column(db.Text, nullable=False)
    answer = db.Column(db.String(255))

    quest_chapter_id = db.Column(db.Integer, db.ForeignKey("quest_chapter.id", ondelete='CASCADE'), nullable=False)
