from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class NewNoteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Note Here", validators=[DataRequired()])
    submit = SubmitField("Save Note")
