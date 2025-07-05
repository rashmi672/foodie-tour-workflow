import os
import uuid
from typing import List, Dict
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Connect to MongoDB 
MONGO_URI = os.getenv("MONGO_URI")  # connection string
MONGO_DB = os.getenv("MONGO_DB")    # db name
client = MongoClient(MONGO_URI)     # connect to MongoDB
db = client[MONGO_DB]               # select the database
collection = db["foodie_tours"]     # select the collection

# Store foodie tour data in MongoDB as history

def insert_foodie_tour(city, text):
    """
    Insert a foodie tour document into the MongoDB collection.
    
    :param tour_data: Dictionary containing the foodie tour data.
    :return: The inserted document's ID.
    """
    result = collection.insert_one({
            "id": str(uuid.uuid4()),
            "city": city,
            "narrative": text,
            "timestamp": datetime.utcnow()
            })
    
from bson import ObjectId
from datetime import datetime

def delete_foodie_tour(id: str) -> bool:
    try:
        result = collection.delete_one({"id": id})
        return result.deleted_count > 0
    except Exception as e:
        raise RuntimeError(f"Error deleting record: {str(e)}")
    
def fetch_history() -> List[Dict]:
    try:
        return list(
            collection.find({}, {"_id": 0})
            .sort("timestamp", -1)
        )
    except Exception as e:
        raise RuntimeError(f"Error fetching foodie tour history: {str(e)}")