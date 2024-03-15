# Built-in
from typing import Any

# Django
from django.db.models.query import QuerySet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.mixins import DestroyModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet

# Application
from jobs.enums import ExecutionStatus
from jobs.tasks import execute_job

# Local
from .models import Execution, Job
from .serializers import ExecutionSerializer, JobSerializer


class JobViewSet(ModelViewSet):
    serializer_class = JobSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet["Job"]:
        user = self.request.user
        organization = user.profile.organization
        return Job.objects.filter(organization=organization)

    @action(detail=True, methods=["get"])
    def manual_launch(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        execution = Execution.objects.create(
            job=instance, status=ExecutionStatus.PENDING
        )
        execute_job.delay(execution_id=execution.id, job_type=instance.type)
        return Response(status=status.HTTP_201_CREATED)


class ExecutionViewSet(GenericViewSet, DestroyModelMixin):
    queryset = Execution.objects.all()
    serializer_class = ExecutionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet["Execution"]:
        user = self.request.user
        organization = user.profile.organization
        return Execution.objects.filter(job__organization=organization)
