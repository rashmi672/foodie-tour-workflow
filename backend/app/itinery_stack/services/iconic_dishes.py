#iconic_dishes.py
import requests
import os
import json
from dotenv import load_dotenv
load_dotenv() 

TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

def get_iconic_dishes(city):
    prompt = (
        f"Respond ONLY in JSON. List exactly 3 iconic dishes from {city} "
        "as an array of strings in the 'dishes' key. "
        "Example: {\"dishes\": [\"Dish1\", \"Dish2\", \"Dish3\"]}. "
        "No explanation or commentary."
    )
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}"
    }
    json_data = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
        "prompt": prompt,
        "max_tokens": 100
    }
    r = requests.post("https://api.together.xyz/v1/completions", headers=headers, json=json_data)
    text = r.json()['choices'][0]['text']
    print("raw text in get_iconic_dishes:", text)
    try:
        json_start = text.find('{')
        json_text = text[json_start:]
        data = json.loads(json_text)
        return data.get("dishes", [])
    except Exception as e:
        print("JSON parsing error:", e)
        return [text.strip()]