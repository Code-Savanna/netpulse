from celery import Celery
import os

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://netpulse:password@rabbitmq:5672//")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://redis:6379/1")

celery_app = Celery(
    "monitoring_tasks",
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND,
    include=["tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_routes={
        'monitor_devices_task': {'queue': 'monitoring'},
    },
    beat_schedule={
        'monitor-devices-every-30-seconds': {
            'task': 'monitor_devices_task',
            'schedule': 30.0,
            'options': {'queue': 'monitoring'}
        },
    }
)
