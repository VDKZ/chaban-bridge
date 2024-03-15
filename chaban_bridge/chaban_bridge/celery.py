# Built-in
import os

# Third-party
from celery import Celery, Task

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.getenv("DJANGO_SETTINGS_MODULE", "chaban_bridge.settings.development"),
)

celery_app = Celery("chaban_bridge")

celery_app.config_from_object("django.conf:settings", namespace="CELERY")

celery_app.autodiscover_tasks()


@celery_app.task(bind=True, ignore_result=True)
def debug_task(self: Task) -> None:
    print(f"Request: {self.request!r}")
