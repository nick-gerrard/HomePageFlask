import requests, json

home_url = "https://api.nytimes.com/svc/topstories/v2/home.json?api-key="
api_key = "rXSAfFC7RwK9xY9HJmfDiZoW4xqs45ZK"
legitimate_url = home_url + api_key

def get_stories(url):
    list_of_stories = []
    r = requests.get(url)
    x = r.json()
    y = x["results"]
    for value in y:
        temp_dict = {
            "title": value["title"],
            "abstract": value["abstract"],
            "url": value["url"],
            "picture_url": value["multimedia"][0]["url"]
        }
        list_of_stories.append(temp_dict)
    return list_of_stories

    