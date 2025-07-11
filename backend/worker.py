# backend/worker.py
from core.config import settings
from celery import Celery

# Create the Celery app instance using URLs from the centralized settings
celery_app = Celery(
    __name__,
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.update(
    task_track_started=True,
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

# Autodiscover tasks
celery_app.autodiscover_tasks(['backend.tasks'])
