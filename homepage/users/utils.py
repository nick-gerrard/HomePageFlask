import json
import requests
from random import randint

def get_json_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

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
 
