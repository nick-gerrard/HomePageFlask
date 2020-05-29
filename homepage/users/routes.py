from flask import Blueprint
import os
from flask import Flask, Response, render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message as ExternalMessage
from homepage import db, bcrypt,  mail
from homepage.users.forms import (RegistrationForm, LoginForm, LinkForm, DeleteLinkForm, 
                                ChangeWeatherForm, RequestResetForm, ResetPasswordForm)
from homepage.models import User, Link, Message
from homepage.users.utils import get_json_data, generate_quote, check_address

users = Blueprint('users', __name__)

@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, 
                    password=hashed_password, zip_code=form.zip_code.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created - you can now log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title="Register", form=form, quote_tuple=quote_tuple)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('main.home'))
        else:
            flash('Login Failed. Check password/email!', 'danger')
    return render_template('login.html', title="Login", form=form, quote_tuple=quote_tuple)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

@users.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    link_form = LinkForm()
    weather_form = ChangeWeatherForm()
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")
    # Link Form Validation
    if link_form.validate_on_submit():
        link = Link(title=link_form.name.data, address=link_form.address.data, user_id=current_user.id)
        if check_address(link_form.address.data) == "VALID":
            db.session.add(link)
            db.session.commit()
            flash("Link Added", 'success')
            return redirect(url_for('users.account'))
        else:
            flash("Invalid URL - try again. Make sure to add \"https://\"", "danger")
        return redirect(url_for('users.account'))
    
    # Change Weather Form Validation
    elif weather_form.validate_on_submit():
        zip_code = str(weather_form.zip_code.data)
        current_user.zip_code = zip_code
        db.session.commit()
        flash("Zip Code Updated", 'success')
        return redirect(url_for('users.account'))

    return render_template('account.html', title="Account", quote_tuple=quote_tuple, link_form=link_form, weather_form=weather_form)



def send_reset_email(user):
    token = user.get_reset_token()
    msg = ExternalMessage('Password Reset Request',
                sender='noreply@HomePagePasswordReset.com', \
                recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request, then simply ignore this email, and no changes will be made to your account.
This link will expire 15 minutes after the request is made.
"""
    mail.send(msg)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")

    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instruction to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', quote_tuple=quote_tuple, title='Reset Passwrod', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been successfully reset.', 'success')
        return redirect(url_for('users.login'))

    return render_template("reset_token.html", quote_tuple=quote_tuple, title="Reset Password", form=form)