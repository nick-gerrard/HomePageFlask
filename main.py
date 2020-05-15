import os
from flask import Flask, Response, render_template, url_for, redirect, flash, request
import requests
import datetime
import lxml
from bs4 import BeautifulSoup
import time
import json
import openweather


news_url = "https://www.nytimes.com/sitemaps/new/news.xml.gz"
weather_url = "https://www.wunderground.com/hourly/us/va/arlington/22204"

def get_weather():
    return openweather.get_arlington_weather(openweather.full_arlington_url)

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

    
def get_trending(news_url):
    trending = []
    r = requests.get(news_url)
    soup = BeautifulSoup(r.content, "lxml")
    urls = soup.find_all("url")
    for url in urls[0:5]:
        trending.append((url.find("loc").get_text(), url.find("news:title").get_text()))
    return trending

app = Flask(__name__)


@app.route("/")
@app.route("/nick")
def nick():
    name = "nick"
    path_to_links = os.getcwd() + "/static/users/" + name + "/links.json"
    links = get_json_data(path_to_links)
    path_to_notes = os.getcwd() + "/static/users/" + name + "/notes.json"
    notes = get_json_data(path_to_notes)
    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")
    trending_stories = get_trending(news_url)
    greeting_type = greeting(name.title())
    weatherdata = get_weather()
    return render_template('nick.html', weatherdata=weatherdata, links=links, greeting=greeting_type, 
                            trending_stories=trending_stories, open_time=open_time, weather_url = weather_url, notes=notes)

@app.route('/new_note')
def new_note():
    name = "nick"
    greeting_type = greeting(name.title())
    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")
    return render_template("new_note.html", greeting=greeting_type, open_time=open_time, title="New Note")