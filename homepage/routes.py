import os, requests, datetime, lxml, time, json
from flask import Flask, Response, render_template, url_for, redirect, flash, request, abort
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
from bs4 import BeautifulSoup
from homepage import app, db, bcrypt,  nyt, openweather
from homepage.forms import RegistrationForm, LoginForm, LinkForm, DeleteLinkForm, NewNoteForm, \
                        ChangeWeatherForm, NewMessageForm
from homepage.models import User, Note, Link, Message


weather_url = "https://www.wunderground.com/hourly/us/va/arlington/22204"
FORMAT = 'utf-8'

def get_news():
    return nyt.get_stories(nyt.legitimate_url)

def get_json_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

def greeting(name):
    return "Hello, " + name

def generate_quote(quote_json):
    quote_list = get_json_data(quote_json)["quotes"]
    num = randint(0, len(quote_list) - 1)
    quote = quote_list[num]["quote"]
    author = quote_list[num]["author"]
    return (quote, author)

def check_address(url):
    try:
        r = requests.get(url)
        return "VALID"
    except:
        return "ERROR"

def coerce_recipient_username(recipient_data):
    x = recipient_data.split("'")
    return x[1]



@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated == False:
        return redirect(url_for('login'))
    # Name and Greeting
    name = current_user.username
    greeting_type = greeting(name.title())

    # Favorite Links
    #path_to_links = os.getcwd() + "/homepage/static/users/" + name + "/links.json"
    #links = get_json_data(path_to_links)
    links = current_user.links

    # Fav Icons (beta)
    """ path_to_favicons = os.getcwd() + "/static/users/" + name + "/favicons.json"
    favicons = get_json_data(path_to_favicons) """

    # Notes
    #path_to_notes = os.getcwd() + "/homepage/static/users/" + name + "/notes.json"
    #notes = get_json_data(path_to_notes)
    notes = current_user.notes

    # Time
    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")

    # Data
    trending_stories = get_news()[0:5]
    weather_url = openweather.get_full_url(current_user.zip_code)
    weatherdata = openweather.get_weather(weather_url)

    # Unread Messages
    messages = Message.query.filter_by(recipient_id=current_user.id)
    for message in messages:
        if message.unread == True:
            flash("You have unread messages", "info")
            break

    return render_template('home.html', weatherdata=weatherdata, links=links, greeting=greeting_type, 
                            trending_stories=trending_stories, open_time=open_time, 
                            weather_url = weather_url, notes=notes)

@app.route("/about")
def about():
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")
    return render_template("about.html", title="About this site", quote_tuple=quote_tuple)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(FORMAT)
        user = User(username=form.username.data, email=form.email.data, 
                    password=hashed_password, zip_code=form.zip_code.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created - you can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form, quote_tuple=quote_tuple)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Check password/email!', 'danger')
    return render_template('login.html', title="Login", form=form, quote_tuple=quote_tuple)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/account', methods=['GET', 'POST'])
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
            return redirect(url_for('account'))
        else:
            flash("Invalid URL - try again. Make sure to add \"https://\"", "danger")
        return redirect(url_for('account'))
    
    # Change Weather Form Validation
    elif weather_form.validate_on_submit():
        zip_code = str(weather_form.zip_code.data)
        current_user.zip_code = zip_code
        db.session.commit()
        flash("Zip Code Updated", 'success')
        return redirect(url_for('account'))

    return render_template('account.html', title="Account", quote_tuple=quote_tuple, link_form=link_form, weather_form=weather_form)

@app.route('/links/<int:user_id>/add', methods=['POST'])
@login_required
def add_link(user_id):
    form = LinkForm()
    if form.validate_on_submit():
        link = Link(title=form.name.data, address=form.address.data, user_id=current_user.id)
        db.session.add(link)
        db.session.commit()
        flash("Link Added", 'success')
    return redirect(url_for('account'))

@app.route('/links/<int:link_id>/delete', methods=['POST'])
@login_required
def remove_link(link_id):
    link = Link.query.get_or_404(link_id)
    if link.author != current_user:
        abort(403)
    db.session.delete(link)
    db.session.commit()
    flash("Link Deleted", 'success')
    return redirect(url_for('account'))

@app.route('/news')
def news():
    name = current_user.username
    greeting_type = greeting(name.title())

    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")

    trending_stories = get_news()[0:20]
    return render_template('news.html', title="News", trending_stories=trending_stories, 
                            open_time=open_time, greeting=greeting_type)

@app.route('/new_note', methods=['GET', 'POST'])
@login_required
def new_note():
    name = current_user.username
    greeting_type = greeting(name.title())

    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")

    form = NewNoteForm()
    if form.validate_on_submit():
        note = Note(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_note.html", greeting=greeting_type, open_time=open_time, 
                            title="New Note", form=form)

@login_required
@app.route('/notes')
def view_notes():
    return(render_template('notes.html', notes=current_user.notes))

@login_required
@app.route("/notes/<int:note_id>", methods=['GET', 'POST'])
def edit_note(note_id):
    note = Note.query.get_or_404(note_id)
    if current_user.id != note.user_id:
        abort(403)
    form = NewNoteForm()
    if form.validate_on_submit():
        note.content = form.content.data
        note.title = form.title.data
        db.session.commit()
        flash("Your Note has been Updated", "success")
        return redirect(url_for('view_notes'))
    elif request.method == 'GET':
        form.title.data = note.title
        form.content.data = note.content
    return render_template('edit_note.html', title=note.title, note=note, form=form)

@login_required
@app.route('/notes/<int:note_id>/delete', methods=['POST'])
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if current_user.id != note.user_id:
        abort(403)
    db.session.delete(note)
    db.session.commit()
    flash('Your Note has been deleted!', 'info')
    return redirect(url_for('home'))

@login_required
@app.route('/view_messages')
def view_messages():
    message_list = []
    user = User.query.get(current_user.id)
    sent_messages = user.sent_messages
    for message in sent_messages:
        sender = current_user.username
        message_list.append((message, sender))
    for message in Message.query.filter_by(recipient_id=current_user.id):
        message.unread = False
        db.session.commit()
        sender = User.query.get(message.sender_id).username
        message_list.append((message, sender))
    return render_template('view_messages.html', messages=message_list)

@app.route('/new_message', methods=['GET', 'POST'])
@login_required
def new_message():
    name = current_user.username
    greeting_type = greeting(name.title())

    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")
    form = NewMessageForm()
    
    if form.validate_on_submit():
        print("validated")
        recipient_username = coerce_recipient_username(form.recipient.data)
        print(recipient_username)
        recipient_id_number = User.query.filter_by(username=recipient_username).first().id
        message = Message(sender_id=current_user.id, subject=form.subject.data, 
                            body=form.body.data, sender=current_user, recipient_id=recipient_id_number)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("new_message.html", greeting=greeting_type, open_time=open_time, 
                            title="New Note", form=form)

@login_required
@app.route('/messages/<int:message_id>/')
def view_message(message_id):
    message = Message.query.get_or_404(message_id)
    print(message.recipient_id, current_user.id)
    if current_user.id != message.recipient_id and current_user.id != message.sender_id:
        abort(403)
    sender = User.query.get(message.sender_id).username
    return render_template('message.html', message=message, sender=sender)