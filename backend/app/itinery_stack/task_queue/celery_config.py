from celery import Celery
from itinery_stack.message_queue.rabbit_config import get_rabbitmq_url
from itinery_stack.database.redis_config import get_redis_url
from dotenv import load_dotenv
load_dotenv()   

def make_celery(app_name="itinery_task_app") -> Celery:
    celery = Celery(
        app_name,
        broker=get_rabbitmq_url(),
        backend=get_redis_url(),
        include=["itinery_stack.task_queue.tasks"]
    )

    celery.conf.update(
        task_serializer="json",
        result_serializer="json",
        accept_content=["json"],
        timezone="UTC",
        enable_utc=True,
    )

    return celery