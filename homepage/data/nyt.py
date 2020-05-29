import requests, json


def get_json_data(file):
    f = open(file)
    data = json.load(f)
    f.close()
    return data

api_key = get_json_data('/configs/HomePageConfigsAPIKeys.json')['NYT_API_KEY']
home_url = "https://api.nytimes.com/svc/topstories/v2/home.json?api-key="
legitimate_url = home_url + api_key


def get_stories(url):
    list_of_stories = []
    r = requests.get(url)
    x = r.json()
    y = x["results"]
    for value in y:
        try:
            temp_dict = {
                "title": value["title"],
                "abstract": value["abstract"],
                "url": value["url"],
                "image_url": value["multimedia"][0]["url"]
            }
            list_of_stories.append(temp_dict)
        except:
            pass
    return list_of_stories

    