from celery import Celery

# Create the Celery app instance
celery_app = Celery(
    "tasks_manager",  # Use the app name
    broker="pyamqp://guest:guest@localhost//",  # RabbitMQ connection string
    backend="rpc://",  # Use RabbitMQ as the result backend
)

# Celery configuration
celery_app.conf.task_routes = {"tasks_manager.tasks.*": {"queue": "default"}}
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
)

# Optional: Beat scheduler configuration will go here if periodic tasks are added
