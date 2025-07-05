#fetch_weather.py
import requests
import os
from dotenv import load_dotenv
load_dotenv() 

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

def get_today_weather(city):
    resp = requests.get(
        "http://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}
    ).json()
    return {
        "description": resp["weather"][0]["description"],
        "temp": resp["main"]["temp"],
        "rain": any(w["main"].lower() in ["rain", "drizzle"] for w in resp["weather"])
    }
