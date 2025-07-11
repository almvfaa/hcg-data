# backend/worker.py
import os
from celery import Celery

# Get the broker and backend URLs from environment variables, with defaults.
# This makes the configuration flexible for different environments.
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

# Create the Celery application instance.
# The first argument is the name of the current module.
celery_app = Celery(
    __name__,
    broker=CELERY_BROKER_URL,
    backend=CELERY_RESULT_BACKEND
)

# It's a good practice to use a separate namespace for Celery settings in your main config.
celery_app.conf.update(
    # By default, Celery will not track when a task starts.
    # This is useful for monitoring.
    task_track_started=True,
    
    # Using JSON as the serializer is a security best practice.
    # Pickle is discouraged due to potential security vulnerabilities.
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
)

# Autodiscover tasks from a 'tasks' module within your project.
# You will create a 'tasks' directory and place your task definitions there.
celery_app.autodiscover_tasks(['backend.tasks'])
