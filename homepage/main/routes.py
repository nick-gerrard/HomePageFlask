import os
from flask import Blueprint
from flask import Flask, Response, render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from homepage import db
from homepage.models import User, Note, Link, Message
from homepage.data import nyt, openweather
from homepage.data.utils import get_news
from homepage.users.utils import generate_quote

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    if current_user.is_authenticated == False:
        return redirect(url_for('users.login'))
    # Links
    links = current_user.links

    # Notes
    notes = current_user.notes

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

    return render_template('home.html', weatherdata=weatherdata, links=links, trending_stories=trending_stories, 
                            weather_url = weather_url, notes=notes)

@main.route("/about")
def about():
    quote_tuple = generate_quote(os.getcwd() + "/homepage/static/quotes.json")
    return render_template("about.html", title="About this site", quote_tuple=quote_tuple)

