# Third-party
from user.models import Organization

# Django
from django.db import models
from django.db.models.fields.related import ForeignKey

# Application
from core.models import LifeCycleModel
from jobs.enums import ExecutionStatus, JobFrequency, JobType


class Job(LifeCycleModel):
    organization = ForeignKey(
        Organization, null=False, on_delete=models.CASCADE, related_name="jobs"
    )
    name = models.CharField(max_length=50)
    type = models.CharField(
        max_length=25,
        choices=JobType.choices,
        default=JobType.CHABAN,
        blank=True,
    )
    frequency = models.CharField(
        max_length=25,
        choices=JobFrequency.choices,
        default=JobFrequency.DAILY,
        blank=True,
    )

    class Meta:
        unique_together = ("organization", "name")

    def __str__(self) -> str:
        return self.name


class Execution(LifeCycleModel):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name="executions")
    status = models.CharField(
        max_length=25,
        choices=ExecutionStatus.choices,
        default=ExecutionStatus.PENDING,
        blank=True,
    )
    result = models.JSONField(default=dict, blank=True)
