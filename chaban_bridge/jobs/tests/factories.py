# Third-party
import factory

# Application
from jobs.enums import ExecutionStatus, JobFrequency, JobType
from jobs.models import Execution, Job


class JobFactory(factory.django.DjangoModelFactory):
    name = "Mon Pont Chaban"
    type = JobType.CHABAN
    frequency = JobFrequency.DAILY

    class Meta:
        model = Job


class ExecutionFactory(factory.django.DjangoModelFactory):
    job = factory.SubFactory(JobFactory)
    status = ExecutionStatus.PENDING
    result = {}

    class Meta:
        model = Execution
