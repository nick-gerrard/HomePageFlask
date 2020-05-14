import requests
from bs4 import BeautifulSoup

weather_url = "https://patch.com/virginia/arlington-va/weather"

def get_temp(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    div = soup.find("div", {"class": "weather-current-temp temperature above-48 inline-block"})
    current_temp = div.text
    # There's room in here to find quite a bit more data, like conditions, future temps, etc.
    return current_temp

news_url = "https://www.nytimes.com/sitemaps/new/news.xml.gz"

def get_trending(news_url):
    trending = []
    r = requests.get(news_url)
    soup = BeautifulSoup(r.content, "xml")
    urls = soup.find_all("url")
    for url in urls[0:5]:
        trending.append((url.find("loc").get_text(), url.find("news:title").get_text()))
    return trending

print(get_trending(news_url))    