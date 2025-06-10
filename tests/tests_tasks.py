from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tasks.models import Comment, Task
from users.models import User


class TaskTestCase(APITestCase):
    """Tests for the Task API."""

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

    def test_task_create(self):
        """Testing the creation of a new task."""
        url = reverse("task:task-list")
        data = {
            "title": "New task",
            "description": "New task description",
            "status": "open",
            "deadline": "2025-07-06",
            "task_performer": self.user_role.pk,
        }

        response = self.client_1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.count(), 2)

        response = self.client_2.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_task_retrieve(self):
        """Testing the viewing of a single issue."""
        url = reverse("task:task-detail", args=(self.task_1.pk,))
        response = self.client_1.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.task_1.title)
        self.assertEqual(data.get("comments"), [])

    def test_task_update(self):
        """Testing the issue update."""
        url = reverse("task:task-detail", args=(self.task_1.pk,))
        data = {"status": "completed"}

        response = self.client_1.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.task_1.status, "open")

        response = self.client_2.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("status"), "completed")

    def test_task_delete(self):
        """Testing task deletion."""
        url = reverse("task:task-detail", args=(self.task_1.pk,))

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Task.objects.count(), 2)

        response = self.client_2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

    def test_task_list(self):
        """Testing the task list view."""
        url = reverse("task:task-list")
        response = self.client_2.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)


class CommentTestCase(APITestCase):
    """Tests for the Comment API."""

    def setUp(self):
        """Environment for the tests."""
        self.user_role = User.objects.create(email="user@test.test", role="user")
        self.manager_role = User.objects.create(
            email="manager@test.test", role="manager"
        )

        self.client.force_authenticate(user=self.user_role)

        self.task = Task.objects.create(
            title="Test task",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager_role,
            task_performer=self.user_role,
        )
        self.comment = Comment.objects.create(
            text="Test comment", task=self.task, created_at=timezone.now()
        )

    def test_comment_create(self):
        """Testing the creation of a new comment."""
        url = reverse("task:comment-list")
        data = {
            "text": "New comment",
            "task": self.task.pk,
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)

    def test_comment_retrieve(self):
        """Testing the viewing of a single comment."""
        url = reverse("task:comment-detail", args=(self.comment.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), self.comment.text)
        self.assertEqual(data.get("task"), self.task.pk)

    def test_comment_update(self):
        """Testing the comment update"""
        url = reverse("task:comment-detail", args=(self.comment.pk,))
        data = {"text": "add something"}

        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("text"), "add something")

    def test_comment_delete(self):
        """Testing the deletion of a comment."""
        url = reverse("task:comment-detail", args=(self.comment.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.count(), 0)

    def test_comment_list(self):
        """Testing the review of the list of comments."""
        url = reverse("task:comment-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
