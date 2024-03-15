# Third-party
import factory
from user.tests.factories import OrganizationFactory

# Application
from jobs.enums import ExecutionStatus, JobFrequency, JobType
from jobs.models import Execution, Job


class JobFactory(factory.django.DjangoModelFactory):
    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Sequence(lambda x: f"job n{x}")
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
