# Third-party
from user.tests.factories import OrganizationFactory, UserFactory

# Django
from django.test import TestCase, override_settings

# Application
from jobs.enums import ExecutionStatus, JobFrequency
from jobs.tasks import daily_jobs, execute_job, weekly_jobs
from jobs.tests.factories import ExecutionFactory, JobFactory


class JobTasksTestCase(TestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.organization = OrganizationFactory(name="test organization")
        self.organization.profiles.add(self.user.profile)
        self.daily_job = JobFactory(organization=self.organization)
        self.weekly_job = JobFactory(
            organization=self.organization, frequency=JobFrequency.WEEKLY
        )

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_daily_jobs(self) -> None:
        executions = self.daily_job.executions.all()
        self.assertEqual(len(executions), 0)

        daily_jobs()

        executions = self.daily_job.executions.all()
        self.assertEqual(len(executions), 1)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_weekly_jobs(self) -> None:
        executions = self.weekly_job.executions.all()
        self.assertEqual(len(executions), 0)

        weekly_jobs()

        executions = self.weekly_job.executions.all()
        self.assertEqual(len(executions), 1)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_execute_job(self) -> None:
        execution = ExecutionFactory(job=self.daily_job)
        self.assertEqual(execution.status, ExecutionStatus.PENDING)

        execute_job(execution.id, self.daily_job.type)

        execution.refresh_from_db()
        self.assertEqual(execution.status, ExecutionStatus.EXECUTED)
