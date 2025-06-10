from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from evaluations.models import Evaluation
from tasks.models import Task
from users.models import User


class UserTestCase(APITestCase):
    """Tests for the User API"""

    def setUp(self):
        """Environment for the tests."""
        self.user_role = User.objects.create(
            email="user@test.test",
            role="user",
            first_name="User",
            last_name="Test"
        )
        self.manager_role = User.objects.create(
            first_name="Manager",
            last_name="Test",
            email="manager@test.test", role="manager"
        )
        self.client.force_authenticate(user=self.user_role)

    def test_user_create(self):
        """Testing the creation of a new user."""
        url = reverse("user:register")
        data = {
            "email": "admin@test.test",
            "role": "admin",
            "password": "securepassword123",
            "first_name": "Admin",
            "last_name": "User",
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)

    def test_user_update(self):
        """Testing the user profile update."""
        url = reverse("user:update_user", args=(self.user_role.pk,))
        data = {"email": "user@update.test"}
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("email"), "user@update.test")

    def test_user_not_owner_update(self):
        """Testing access rights to update the user's profile."""
        url = reverse("user:update_user", args=(self.manager_role.pk,))
        data = {"email": "manager@update.test"}
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.manager_role.email, "manager@test.test")

    def test_user_delete(self):
        """Testing user deletion."""
        url = reverse("user:delete_user", args=(self.user_role.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

    def test_user_not_owner_delete(self):
        """Testing access rights to delete a user."""
        url = reverse("user:delete_user", args=(self.manager_role.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 2)

    def test_user_list(self):
        """Testing the user list view."""
        url = reverse("user:users_list")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.user_role.id,
                "email": "user@test.test",
                "first_name": "User",
                "last_name": "Test",
                "role": "user",
                "is_active": True,
            },
            {
                "id": self.manager_role.id,
                "email": "manager@test.test",
                "first_name": "Manager",
                "last_name": "Test",
                "role": "manager",
                "is_active": True,
            },
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
        self.assertEqual(len(data), 2)


class UserAverageScoreTestCase(APITestCase):
    """Tests for the model of obtaining the average user score."""

    def setUp(self):
        self.user = User.objects.create(email="user@test.test", role="user")
        self.manager = User.objects.create(email="manager@test.test", role="manager")

        self.task_1 = Task.objects.create(
            title="Manager task",
            description="Some description",
            status="open",
            deadline="2025-08-06",
            author=self.manager,
            task_performer=self.manager,
        )
        self.task_2 = Task.objects.create(
            title="User task",
            description="Some description",
            status="in-progress",
            deadline="2025-06-05",
            author=self.manager,
            task_performer=self.user,
        )
        self.task_3 = Task.objects.create(
            title="User task_2 ",
            description="Some description",
            status="in-progress",
            deadline="2025-07-06",
            author=self.manager,
            task_performer=self.user,
        )
        self.evaluation_1 = Evaluation.objects.create(
            task=self.task_1, author=self.manager, score=2, created_at=timezone.now()
        )
        self.evaluation_2 = Evaluation.objects.create(
            task=self.task_2, author=self.manager, score=3, created_at=timezone.now()
        )
        self.evaluation_3 = Evaluation.objects.create(
            task=self.task_3, author=self.manager, score=5, created_at=timezone.now()
        )

        self.client.force_authenticate(user=self.user)

    def test_user_average_score_retrieve(self):
        """Testing the user's average rating review."""
        url = reverse("user:user_average_score", args=(self.user.pk,))
        start_date = timezone.now() - timezone.timedelta(days=1)
        end_date = timezone.now() + timezone.timedelta(days=1)
        response = self.client.get(
            url,
            {"start": start_date, "end": end_date},
        )
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("average_score"), 4)
