from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["app.core.background_tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    beat_schedule={
        'monitor-devices-every-30-seconds': {
            'task': 'monitor_devices_task',
            'schedule': 30.0,
        },
    }
)

if __name__ == "__main__":
    celery_app.start()
