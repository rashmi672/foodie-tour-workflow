import os
from dotenv import load_dotenv
load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASS = os.getenv("RABBITMQ_PASS")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_VHOST = os.getenv("RABBITMQ_VHOST")

def get_rabbitmq_url():
    """
    Constructs the RabbitMQ URL using environment variables.
    Returns:
        str: The RabbitMQ URL in the format 'amqp://user:password@host:port/vhost'.
    """
    print("Constructed RabbitMQ URL.")
    return f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VHOST}"
