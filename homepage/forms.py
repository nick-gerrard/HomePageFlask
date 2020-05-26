import requests, os, json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from homepage.models import User, Link, Message
from homepage import db


class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email =  StringField('Email',
                            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    zip_code = IntegerField("Zip Code", validators=[DataRequired()])
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
             raise ValidationError('That username is taken, please select another')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
             raise ValidationError('There is already an account attached to that email.')
        
    def validate_zip_code(self, zip_code):
        f = open(os.getcwd() + "/homepage/static/valid-zips.json")
        data = json.load(f)
        f.close()
        print(zip_code.data)
        if str(zip_code.data) in data:
            print("Found zip code")
            return
        else:
            raise ValidationError("That zip code is invalid. Please enter a valid 5 digit zip code.")

class LoginForm(FlaskForm):
    email =  StringField('Email',
                            validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField("Log In")

class LinkForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    address = StringField('WebAddress:', validators=[DataRequired()])
    submit = SubmitField("Add Link")

class DeleteLinkForm(FlaskForm):
    links = SelectField("Select a link to remove", choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    submit = SubmitField("Remove Link")

class NewNoteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Note Here", validators=[DataRequired()])
    submit = SubmitField("Save Note")

class ChangeWeatherForm(FlaskForm):
    zip_code = IntegerField("Zip Code", validators=[DataRequired()])
    submit = SubmitField("Change Zip?")

    def validate_zip_code(self, zip_code):
        f = open(os.getcwd() + "/homepage/static/valid-zips.json")
        data = json.load(f)
        f.close()
        print(zip_code.data)
        if str(zip_code.data) in data:
            print("Found zip code")
            return
        else:
            raise ValidationError("That zip code is invalid. Please enter a valid 5 digit zip code.")


class NewMessageForm(FlaskForm):
    recipient = StringField("Username", validators=[DataRequired()])
    subject = StringField("Subject", validators=[DataRequired()])
    body = TextAreaField("Note Here", validators=[DataRequired()])
    submit = SubmitField("Send Message")
