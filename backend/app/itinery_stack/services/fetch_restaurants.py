# fetch_restaurants.py
import requests
import os
import json
import time
from dotenv import load_dotenv
load_dotenv() 

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def get_best_restaurant(city, dish):
    prompt = (
        f"Provide EXACTLY ONE real or typical top-rated restaurant in {city} that serves {dish}. "
        "Respond ONLY in JSON with keys: name, rating, address. "
        "Example: {\"name\": \"Example Restaurant\", \"rating\": 4.5, \"address\": \"123 Main St\"}. "
        "No explanation or commentary."
    )
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}"
    }
    json_data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 150
    }
    for attempt in range(3):
        try:
            r = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=json_data)
            resp_json = r.json()
            print(f"LLM response: {resp_json}")
            text = resp_json['choices'][0]['text']
            print("raw text in get_best_restaurant:", text)
            json_start = text.find('{')
            json_text = text[json_start:]
            data = json.loads(json_text)
            return {
                "name": data.get("name"),
                "rating": data.get("rating"),
                "address": data.get("address")
            }
        except Exception as e:
            print(f"Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    # Fallback if all attempts fail
    return {
        "name": f"{dish} Delight",
        "rating": 4.5,
        "address": f"456 {city} Food Street"
    }