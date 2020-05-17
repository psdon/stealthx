from ..extensions import db

quest_book_tags = db.Table("quest_book_tags",
                           db.Column("quest_book_id", db.Integer, db.ForeignKey("quest_book.id", ondelete='CASCADE')),
                           db.Column("tag_id", db.Integer, db.ForeignKey("tags.id", ondelete='CASCADE')),
                           )


class QuestBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), nullable=False)
    short_description = db.Column(db.String(225))
    long_description = db.Column(db.Text, nullable=False)
    avatar_url = db.Column(db.Text, nullable=False)
    avatar_orig_filename = db.Column(db.String(255), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=False)

    for_review = db.Column(db.Boolean, nullable=False, default=False)

    quest_master_user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete='CASCADE'), nullable=False)
    tags = db.relationship('Tags', secondary=quest_book_tags, backref='quest_books', lazy='dynamic')
