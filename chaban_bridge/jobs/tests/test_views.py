# Third-party
from user.tests.factories import OrganizationFactory, UserFactory

# Django
from django.test import TestCase, override_settings
from rest_framework.test import APIClient

# Application
from jobs.enums import JobFrequency, JobType
from jobs.models import Execution
from jobs.tests.factories import ExecutionFactory, JobFactory


class JobViewSetTestCase(TestCase):
    viewset_url = "http://0.0.0.0:8000/api/v1/jobs/"

    def setUp(self) -> None:
        self.api_client = APIClient()
        self.user = UserFactory()
        self.organization = OrganizationFactory(name="test organization")
        self.organization.profiles.add(self.user.profile)
        self.job = JobFactory(organization=self.organization)
        self.execution_1 = ExecutionFactory(job=self.job)
        self.execution_2 = ExecutionFactory(job=self.job)
        self.api_client.force_authenticate(user=self.user)

    def test_permission(self) -> None:
        self.api_client.logout()
        response = self.api_client.get(self.viewset_url)
        self.assertEqual(response.status_code, 403)

    def test_list(self) -> None:
        response = self.api_client.get(self.viewset_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["id"], self.job.id)
        self.assertEqual(response.data[0]["name"], self.job.name)
        self.assertEqual(response.data[0]["type"], self.job.type)
        self.assertEqual(response.data[0]["frequency"], self.job.frequency)
        self.assertEqual(response.data[0]["executions"][0]["id"], self.execution_1.id)
        self.assertEqual(
            response.data[0]["executions"][0]["status"], self.execution_1.status
        )
        self.assertEqual(
            response.data[0]["executions"][0]["result"], self.execution_1.result
        )
        self.assertEqual(
            response.data[0]["executions"][0]["created_at"],
            self.execution_1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )

    def test_retrieve(self) -> None:
        url = f"{self.viewset_url}{self.job.pk}/"
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.job.id)
        self.assertEqual(response.data["name"], self.job.name)
        self.assertEqual(response.data["type"], self.job.type)
        self.assertEqual(response.data["frequency"], self.job.frequency)
        self.assertEqual(response.data["executions"][0]["id"], self.execution_1.id)
        self.assertEqual(
            response.data["executions"][0]["status"], self.execution_1.status
        )
        self.assertEqual(
            response.data["executions"][0]["result"], self.execution_1.result
        )
        self.assertEqual(
            response.data["executions"][0]["created_at"],
            self.execution_1.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        )

    def test_retrieve_fail(self) -> None:
        url = f"{self.viewset_url}999/"
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_create(self):
        payload = {
            "organization": self.organization.pk,
            "name": "Weather",
            "type": JobType.CHABAN,
            "frequency": JobFrequency.DAILY,
        }
        response = self.api_client.post(self.viewset_url, data=payload, format="json")
        self.assertEqual(response.status_code, 201)

    def test_create_fail(self) -> None:
        payload = {
            "organization": self.organization.pk,
            "name": "Weather",
            "type": "test",
            "frequency": JobFrequency.DAILY,
        }
        response = self.api_client.post(self.viewset_url, data=payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_update(self) -> None:
        url = f"{self.viewset_url}{self.job.pk}/"
        payload = {
            "organization": self.organization.pk,
            "name": "Mon Pont Chaban updated",
            "type": JobType.CHABAN,
            "frequency": JobFrequency.DAILY,
        }
        response = self.api_client.put(url, data=payload, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Mon Pont Chaban updated")

    def test_update_fail(self) -> None:
        url = f"{self.viewset_url}{self.job.pk}/"
        payload = {
            "organization": self.organization.pk,
            "name": "Mon Pont Chaban",
            "type": "test",
            "frequency": JobFrequency.DAILY,
        }
        response = self.api_client.put(url, data=payload, format="json")
        self.assertEqual(response.status_code, 400)

    def test_delete(self) -> None:
        response = self.api_client.get(self.viewset_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        url = f"{self.viewset_url}{self.job.pk}/"
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, 204)

        response = self.api_client.get(self.viewset_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    @override_settings(CELERY_TASK_ALWAYS_EAGER=True)
    def test_manual_launch(self) -> None:
        executions = self.job.executions.all()
        self.assertEqual(len(executions), 2)

        url = f"{self.viewset_url}{self.job.pk}/manual_launch/"
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, 201)

        executions = self.job.executions.all()
        self.assertEqual(len(executions), 3)


class ExecutionViewSetTestCase(TestCase):
    viewset_url = "http://0.0.0.0:8000/api/v1/executions/"

    def setUp(self) -> None:
        self.user = UserFactory()
        self.api_client = APIClient()
        self.organization = OrganizationFactory(name="test organization")
        self.organization.profiles.add(self.user.profile)
        self.job = JobFactory(organization=self.organization)
        self.execution = ExecutionFactory(job=self.job)
        self.api_client.force_authenticate(user=self.user)

    def test_delete(self) -> None:
        executions = Execution.objects.all()
        self.assertEqual(len(executions), 1)

        url = f"{self.viewset_url}{self.execution.pk}/"
        response = self.api_client.delete(url)
        self.assertEqual(response.status_code, 204)

        executions = Execution.objects.all()
        self.assertEqual(len(executions), 0)
