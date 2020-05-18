import os
from flask import Flask, Response, render_template, url_for, redirect, flash, request
from forms import RegistrationForm, LoginForm
import requests
import datetime
import lxml
from bs4 import BeautifulSoup
import time
import json
import openweather
import nyt


news_url = "https://www.nytimes.com/sitemaps/new/news.xml.gz"
weather_url = "https://www.wunderground.com/hourly/us/va/arlington/22204"

def get_weather():
    return openweather.get_arlington_weather(openweather.full_arlington_url)

def get_news():
    return nyt.get_stories(nyt.legitimate_url)

def get_json_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

def greeting(name):
    full_time = datetime.datetime.now() - datetime.timedelta(hours=4)
    hour = full_time.hour
    if hour < 12:
        greet = "Good Morning, " + str(name)
        return greet
    elif hour < 17:
        greet = "Good Afternoon, " + str(name)
        return greet
    else:
        greet = "Good Evening, " + str(name)
        return greet


app = Flask(__name__)
app.config['SECRET_KEY'] = '37e1b18e528f342f7f510f04d8b00744'


@app.route("/")
@app.route("/home")
def home():
    # Name and Greeting
    name = "nick"
    greeting_type = greeting(name.title())

    # Favorite Links
    path_to_links = os.getcwd() + "/static/users/" + name + "/links.json"
    links = get_json_data(path_to_links)

    # Fav Icons (beta)
    """ path_to_favicons = os.getcwd() + "/static/users/" + name + "/favicons.json"
    favicons = get_json_data(path_to_favicons) """

    # Notes
    path_to_notes = os.getcwd() + "/static/users/" + name + "/notes.json"
    notes = get_json_data(path_to_notes)

    # Time
    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")

    # Data
    trending_stories = get_news()[0:5]
    weatherdata = get_weather()

    return render_template('nick.html', weatherdata=weatherdata, links=links, greeting=greeting_type, 
                            trending_stories=trending_stories, open_time=open_time, 
                            weather_url = weather_url, notes=notes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title="Register", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "nick" and form.password.data == "pass":
            flash('Login Successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Failed. Check password/email!', 'danger')
    return render_template('login.html', title="Login", form=form)

@app.route('/news')
def news():
    name = "nick"
    greeting_type = greeting(name.title())

    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")

    trending_stories = get_news()[0:20]
    return render_template('news.html', title="News", trending_stories=trending_stories, 
                            open_time=open_time, greeting=greeting_type)


@app.route('/new_note')
def new_note():
    name = "nick"
    greeting_type = greeting(name.title())

    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")
    return render_template("new_note.html", greeting=greeting_type, open_time=open_time, 
                            title="New Note")