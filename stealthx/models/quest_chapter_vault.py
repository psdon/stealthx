from stealthx.extensions import db


class QuestChapterVault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.Text)
    video_orig_filename = db.Column(db.Text)
    description = db.Column(db.Text, nullable=False)

    quest_chapter_id = db.Column(db.Integer, db.ForeignKey("quest_chapter.id", ondelete='CASCADE'), nullable=False)