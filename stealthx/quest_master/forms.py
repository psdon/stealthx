import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.datastructures import FileStorage
from wtforms import StringField, HiddenField, TextAreaField, SelectField, Form, FormField, FieldList
from wtforms.validators import DataRequired, Length, ValidationError

from stealthx.models import QuestBook


class QuestBookForm(FlaskForm):
    # _quest_book_obj = None

    def __init__(self, quest_book_obj=None, *args, **kwargs):
        super(QuestBookForm, self).__init__(*args, **kwargs)
        self._quest_book_obj = quest_book_obj

    quest_title = StringField(validators=[Length(max=45), DataRequired(message="Enter quest title")])

    quest_code = StringField(validators=[Length(max=45)])

    avatar_hidden = FileField(validators=[FileAllowed(['jpg', 'jpe', 'jpeg', 'png'], "Please upload a valid image")], )

    # TODO: Length of 255?
    short_description = TextAreaField(validators=[Length(max=225)])

    long_description = TextAreaField(validators=[DataRequired(message="Enter a description")])

    difficulty = SelectField(choices=[("easy", 'Easy'), ("medium", "Medium"), ("hard", "Hard")],
                             validators=[DataRequired(message="Enter your country")])

    meta_tags_hidden = HiddenField(validators=[DataRequired(message="Please enter at least one tag")])

    def validate_avatar_hidden(self, field):
        if not (self._quest_book_obj and self._quest_book_obj.avatar_orig_filename):
            if not (isinstance(field.data, FileStorage) and field.data):
                raise ValidationError("Please upload an avatar")

    @staticmethod
    def validate_quest_code(_, field):
        if not field.data:
            return None

        obj = QuestBook.query.filter_by(code=field.data).first()
        if obj and field.data != obj.code:
            raise ValidationError("This code is already taken")

        if re.findall(r"[^a-zA-Z0-9\-]", field.data):
            raise ValidationError("Only alphabet, numbers, and hyphen are allowed")

        if re.findall(r"^[-]|[-]$", field.data):
            raise ValidationError("Hyphen in the beginning or at the end are not allowed")


class QuestForm(Form):
    quest = StringField(validators=[DataRequired('This is a required field')])
    answer = StringField(validators=[Length(max=255)])


class QuestChapterForm(FlaskForm):
    chapter_title = StringField(validators=[Length(max=45), DataRequired(message="Enter chapter title")])
    video_hidden = FileField(validators=[FileAllowed(['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
                                                     "Please upload a  video file")], )
    description_hidden = StringField(validators=[DataRequired(message="Enter a description")])

    quests = FieldList(FormField(QuestForm), min_entries=1)


class QuestChapterVaultForm(FlaskForm):
    video_hidden = FileField(validators=[FileAllowed(['mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv'],
                                                     "Please upload a  video file")], )
    description_hidden = StringField(validators=[DataRequired(message="Enter a description")])
