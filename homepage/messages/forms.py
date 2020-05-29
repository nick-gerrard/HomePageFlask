from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from homepage.models import User, Message

def generate_user_list():
        return [(user.username, user.username) for user in User.query.all()]
    

class NewMessageForm(FlaskForm):
    recipient = SelectField("Send To:", choices=[], validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    body = TextAreaField("Body", validators=[DataRequired()])
    submit = SubmitField("Send Message")
    
    
