import os
import requests
from .celery_config import make_celery
from dotenv import load_dotenv
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

from itinery_stack.services import get_today_weather, choose_dining, get_best_restaurant, get_iconic_dishes
from itinery_stack.services import speech_generation
from itinery_stack.database.mongo_utils import insert_foodie_tour

# from itinery_stack.services import translate_text

celery_app = make_celery()

@celery_app.task(name="tasks.generate_itinery_task")
def generate_itinery_task(
    city: str,
    language: str
    ):

    try:
        weather = get_today_weather(city)          # returns a dict
        print("weather", weather)
        dining_type = choose_dining(weather)       # returns a str
        print("dining_type", dining_type)
        rain_status = "raining" if weather["rain"] else "not raining"
        print("rain status", rain_status)
        dishes = get_iconic_dishes(city)          # returns a list[str]
        print("dishes", dishes)
        restaurants = [
            f"{rest['name']} with rating {rest['rating']} situated at {rest['address']}"
            for rest in [get_best_restaurant(city, dish) for dish in dishes]
        ]       
        print("restaurants", restaurants)
        prompt = (
            f"Given the city {city} with weather described as {weather['description']}, {weather['temp']} today, and the following three popular dishes described as: {dishes}, "
            f"and the following restaurants: {restaurants}, create a very short, quick to read, fun one-day foodie tour narrative in less than 150 words. Use emojis in few places. "
            f"Decide which dish to serve for 1.breakfast, 2.lunch, and 3.dinner at any of the the restaurants you choose from the lists provided. "
            f"Also mention whether indoor or outdoor dining ({dining_type}) is preferable, since weather is {weather['description']} and {rain_status}, "
            "Keep it very brief and friendly, in less than 100 words, End with a question to the user, like 'Are you ready for this delicious adventure?'"
        )
        headers = {
            "Authorization": f"Bearer {TOGETHER_API_KEY}"
        }
        json_data = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "prompt": prompt,
            "max_tokens": 300
        }
        r = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=json_data)
        text = r.json()['choices'][0]['text'].strip()

        # if language != "English":
            # narrative_text = translate_text(narrative_text, language)
        
        # Store in MongoDB
        insert_foodie_tour(city, text)

        return {
            "city": city,
            "weather": weather,
            "dining_type": dining_type,
            "rain_status": rain_status,
            "dishes": dishes,
            "restaurants": restaurants,
            "narrative": text
        }
    
    except Exception as e:
        print(f">>> [ERROR] Exception occurred: {e}")
        raise ValueError(f"Error during generate food tour: {e}")

    