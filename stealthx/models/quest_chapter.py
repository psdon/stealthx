from ..extensions import db


class QuestChapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    description = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.Text)
    video_orig_filename = db.Column(db.Text)

    quest_book_id = db.Column(db.Integer, db.ForeignKey("quest_book.id", ondelete='CASCADE'), nullable=False)

    quests = db.relationship('Quest', backref='quest_chapter', cascade='all, delete-orphan')
    vault = db.relationship('QuestChapterVault', backref='quest_chapter', cascade='all, delete-orphan', uselist=False)