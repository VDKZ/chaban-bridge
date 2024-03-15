# Django
from django.db import models


class JobType(models.TextChoices):
    CHABAN = "Mon Pont Chaban"
    WEATHER = "Check weather"


class JobFrequency(models.TextChoices):
    DAILY = "Daily"
    WEEKLY = "Weekly"


class ExecutionStatus(models.TextChoices):
    PENDING = "PENDING"
    TO_BE_PROCESSED = "TO BE PROCESSED"
    ON_GOING = "ON GOING"
    EXECUTED = "EXECUTED"
