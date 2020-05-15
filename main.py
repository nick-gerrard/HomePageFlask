from flask import Flask, Response, render_template, url_for
import requests
import datetime
import lxml
from bs4 import BeautifulSoup
import time

news_url = "https://www.nytimes.com/sitemaps/new/news.xml.gz"
weather_url = "https://patch.com/virginia/arlington-va/weather"
links = {"Gmail": "https://www.mail.google.com",
    "F A C E B O O K":"https://www.facebook.com/",
    "YouTube": "https://www.youtube.com",
    "Netflix": "https://www.netflix.com",
    "Hulu" : "https://www.hulu.com"
}



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

def get_temp(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        div = soup.find("div", {"class": "weather-current-temp temperature above-48 inline-block"})
        current_temp = div.text
    except:
        div = soup.find("div", {"class": "weather-current-temp temperature above-62 inline-block"})
        current_temp = div.text
    # There's room in here to find quite a bit more data, like conditions, future temps, etc.
    return current_temp

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
    name = "Nick"
    unadjusted_time = datetime.datetime.now()
    adjusted_time = unadjusted_time - datetime.timedelta(hours=4)
    open_time = adjusted_time.strftime("%Y.%m.%d|%H:%M:%S")
    trending_stories = get_trending(news_url)
    greeting_type = greeting(name)
    temp = get_temp(weather_url)
    return render_template('nick.html', temp=temp, links=links, greeting=greeting_type, 
                            weather_url=weather_url, trending_stories=trending_stories,
                            open_time=open_time)

@app.route('/time_feed')
def time_feed():
    def generate():
        while True:
            yield datetime.datetime.now().strftime("%Y.%m.%d|%H:%M:%S")
            time.sleep(1)
    return Response(generate())
