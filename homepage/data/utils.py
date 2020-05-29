import json, requests
from homepage.data import nyt, openweather

def get_news():
    return nyt.get_stories(nyt.legitimate_url)

def get_json_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

def check_address(url):
    try:
        r = requests.get(url)
        return "VALID"
    except:
        return "ERROR"

