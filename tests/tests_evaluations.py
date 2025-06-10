from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from evaluations.models import Evaluation
from tasks.models import Task
from users.models import User


class EvaluationTestCase(APITestCase):
    """Tests for the Evaluation API."""

    def setUp(self):
        """Environment for the tests."""
        self.client_1 = APIClient()
        self.client_2 = APIClient()

        self.user_role = User.objects.create(email="user@test.test", role="user")
        self.manager_role = User.objects.create(
            email="manager@test.test", role="manager"
        )

        self.client_1.force_authenticate(user=self.user_role)
        self.client_2.force_authenticate(user=self.manager_role)

        self.task_1 = Task.objects.create(
            title="Test task",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager_role,
            task_performer=self.user_role,
        )
        self.task_2 = Task.objects.create(
            title="Some task",
            description="Some description",
            status="in-progress",
            deadline="2025-08-06",
            author=self.manager_role,
            task_performer=self.manager_role,
        )
        self.task_3 = Task.objects.create(
            title="Task without evaluations",
            description="Some description",
            status="in-progress",
            deadline="2025-06-06",
            author=self.manager_role,
            task_performer=self.user_role,
        )
        self.evaluation_1 = Evaluation.objects.create(
            task=self.task_1,
            author=self.manager_role,
            score=5,
            created_at=timezone.now(),
        )
        self.evaluation_2 = Evaluation.objects.create(
            task=self.task_2,
            author=self.manager_role,
            score=3,
            created_at=timezone.now(),
        )

    def test_evaluation_create(self):
        """Testing the creation of a new assessment."""
        url = reverse("evaluation:evaluation-list")
        data = {
            "task": self.task_3.pk,
            "author": self.manager_role.pk,
            "score": 1,
            "created_at": timezone.now(),
        }

        response = self.client_1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Evaluation.objects.count(), 2)

        response = self.client_2.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Evaluation.objects.count(), 3)

    def test_invalid_evaluation_create(self):
        """Testing the creation of invalid estimates."""
        url = reverse("evaluation:evaluation-list")
        data = {
            "task": self.task_1.pk,
            "author": self.user_role.pk,
            "score": 6,
            "created_at": timezone.now(),
        }

        response = self.client_2.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["score"], ["Значения 6 нет среди допустимых вариантов."]
        )
        self.assertEqual(Evaluation.objects.count(), 2)

    def test_evaluation_retrieve(self):
        """Testing the viewing of a single score."""
        url = reverse("evaluation:evaluation-detail", args=(self.evaluation_1.pk,))
        response = self.client_1.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("score"), self.evaluation_1.score)

    def test_evaluation_update(self):
        """Testing the score update."""
        url = reverse("evaluation:evaluation-detail", args=(self.evaluation_1.pk,))
        data = {"score": "2"}

        response = self.client_1.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.evaluation_1.score, 5)

        response = self.client_2.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("score"), 2)

    def test_evaluation_delete(self):
        """Evaluation deletion testing."""
        url = reverse("evaluation:evaluation-detail", args=(self.evaluation_2.pk,))

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Evaluation.objects.count(), 2)

        response = self.client_2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Evaluation.objects.count(), 1)

    def test_evaluation_list(self):
        """
Testing the review of the rating list."""
        url = reverse("evaluation:evaluation-list")
        response = self.client_2.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)
