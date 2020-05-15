import requests, json

arlington_id = "4744725"
api_key = "c9feaa1db7664788e7a117ca3aee9af3"
base_url = "http://api.openweathermap.org/data/2.5/weather?id="
full_arlington_url = base_url + arlington_id + "&appid=" + api_key
#url WHOLE api.openweathermap.org/data/2.5/weather?id={city id}&appid={your api key}
# http://api.openweathermap.org/data/2.5/weather?id=4744725&appid=c9feaa1db7664788e7a117ca3aee9af3

# K to F
# K − 273.15) × 9/5 + 32 = °F

def kelvin_to_fahrenheit(k):
    f = (k - 273.15) * 9/5 + 32
    return int(f)
    
def get_arlington_weather(url):
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
