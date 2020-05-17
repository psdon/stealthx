from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from werkzeug.datastructures import FileStorage
from wtforms import StringField, HiddenField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, ValidationError


class QuestBookForm(FlaskForm):
    # _quest_book_obj = None

    def __init__(self, quest_book_obj=None, *args, **kwargs):
        super(QuestBookForm, self).__init__(*args, **kwargs)
        self._quest_book_obj = quest_book_obj

    quest_title = StringField(validators=[Length(max=45), DataRequired(message="Enter quest title")])

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
