import requests, json

# URL: http://api.openweathermap.org/data/2.5/weather?zip={zip code},{country code}&appid={your api key}


api_key = "c9feaa1db7664788e7a117ca3aee9af3"
base_url = "http://api.openweathermap.org/data/2.5/weather?zip="
#url WHOLE api.openweathermap.org/data/2.5/weather?id={city id}&appid={your api key}
# http://api.openweathermap.org/data/2.5/weather?id=4744725&appid=c9feaa1db7664788e7a117ca3aee9af3


def get_full_url(zip):
    full_url = base_url + str(zip) + "&appid=" + api_key
    return full_url

def kelvin_to_fahrenheit(k):
    f = (k - 273.15) * 9/5 + 32
    f_rounded = int(f * 10) / 10
    return f_rounded
    
def get_weather(url):
    r = requests.get(url)
    x = r.json()
    y = x["main"]
    z = x["weather"][0]
    description = z["description"].title()
    temp = kelvin_to_fahrenheit(y["temp"])
    feels_like = kelvin_to_fahrenheit(y["feels_like"])
    temp_min = kelvin_to_fahrenheit(y["temp_min"])
    temp_max = kelvin_to_fahrenheit(y["temp_max"])
    weather_data = {
                    "temp": temp, 
                    "feels_like": feels_like, 
                    "temp_min": temp_min, 
                    "temp_max": temp_max,
                    "description": description
                    }
    return weather_data
