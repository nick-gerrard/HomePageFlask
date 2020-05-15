import os
from flask import Flask, Response, render_template, url_for
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

def get_links(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

def greeting(name):
    full_time = datetime.datetime.now() - datetime.timedelta(hours=4)
    hour = full_time.hour
    if hour < 12:
        greet = "Good Morning, " + name
        return greet
    elif hour < 17:
        greet = "Good Afternoon, " + name
        return greet
    else:
        greet = "Good Evening, " + name
        return greet

    
def get_trending(news_url):
    trending = []
    r = requests.get(news_url)
    soup = BeautifulSoup(r.content, "lxml")
    urls = soup.find_all("url")
    for url in urls[0:5]:
        trending.append((url.find("loc").get_text(), url.find("news:title").get_text()))
    return trending

def interactive_function():
    name = input("What's your name? ")
    return f"Hello, {name}, I'm a server!"

app = Flask(__name__)


@app.route("/")
@app.route("/nick")
def nick():
    name = "Nick"
    path_to_links = os.getcwd() + "/static/nick_links.json"
    links = get_links(path_to_links)
    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")
    trending_stories = get_trending(news_url)
    greeting_type = greeting(name)
    weatherdata = get_weather()
    return render_template('nick.html', weatherdata=weatherdata, links=links, greeting=greeting_type, 
                            trending_stories=trending_stories, open_time=open_time, weather_url = weather_url)

@app.route('/time_feed')
def time_feed():
    def generate():
        while True:
            #realtime = datetime.datetime.now() - datetime.timedelta(hours=4)
            yield datetime.datetime.now().strftime("%Y.%m.%d|%H:%M:S")
            time.sleep(1)
    return Response(generate(), mimetype='text')

@app.route('/new_note')
def new_note():
    name = "Nick"
    greeting_type = greeting(name)
    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")
    return render_template("new_note.html", greeting=greeting_type, open_time=open_time, title="New Note")