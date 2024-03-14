# Built-in
import os

# Local
from .base import *  # noqa
from .base import (
    POSTGRES_CHABAN_BRIDGE_DB,
    POSTGRES_SERVICE_HOST,
    POSTGRES_SERVICE_PORT,
)

# We use admin user
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": POSTGRES_SERVICE_HOST,
        "PORT": POSTGRES_SERVICE_PORT,
        "USER": POSTGRES_USER,
        "PASSWORD": POSTGRES_PASSWORD,
        "NAME": POSTGRES_CHABAN_BRIDGE_DB,
    }
}
