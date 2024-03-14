# Django
from rest_framework.viewsets import ModelViewSet

# Local
from .models import Job
from .serializers import JobSerializer


class JobViewSet(ModelViewSet):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
