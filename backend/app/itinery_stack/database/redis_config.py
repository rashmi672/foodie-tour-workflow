import os
# LOADING VARIABLES
from dotenv import load_dotenv
load_dotenv()

# REDIS_HOST = os.getenv("REDIS_HOST", "redis") # Default to "redis" for Docker container
REDIS_HOST = os.getenv("REDIS_HOST") # Default to "localhost" for local development
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

def get_redis_url():
    print(f"Using Redis URL: redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}")
    return f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"