# Local
from .base import *  # noqa type: ignore
from .base import ALLOWED_HOSTS

DEBUG = True

ALLOWED_HOSTS += ["host.docker.internal"]

# Channels

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": ["redis://redis:6379/0"],
        },
    },
}

# Celery

CELERY_BROKER_URL = "redis://redis:6379/1"
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
