import os, json
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from homepage.models import User, Link

class RegistrationForm(FlaskForm):
    username = StringField('Username', 
                            validators=[DataRequired(), Length(min=2, max=20)])
    email =  StringField('Email',
                            validators=[DataRequired(), Email()])
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
                            validators=[DataRequired(), Email()])
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

class RequestResetForm(FlaskForm):
    email =  StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account associated with that email. You must register first.")
    
class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', 
                                    validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Reset Password")
