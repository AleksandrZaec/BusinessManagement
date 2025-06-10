from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from meetings.models import Meeting
from tasks.models import Task
from users.models import User


class CalendarTestCase(APITestCase):
    """Tests for calendar."""

    def setUp(self):
        """Environment for the tests."""
        self.user = User.objects.create(email="user@test.test", role="user")
        self.manager = User.objects.create(email="manager@test.test", role="manager")

        self.client.force_authenticate(user=self.user)

        self.task = Task.objects.create(
            title="Test task",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager,
            task_performer=self.user,
        )
        self.task_for_manager = Task.objects.create(
            title="Test task for manager",
            description="Test description",
            status="open",
            deadline="2025-06-06",
            author=self.manager,
            task_performer=self.manager,
        )
        self.meeting = Meeting.objects.create(
            title="Test meeting",
            date="2025-06-06",
            start_time="10:00:00",
            end_time="11:00:00",
            organizer=self.manager,
        )
        self.meeting.participants.set([self.user, self.manager])

        self.url = reverse("calendar:calendar")

    def test_calendar_day_view_success(self):
        """tests that the calendar is returned for the day."""
        data = {"view": "day", "date": "2025-06-05"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tasks", response.data)

    def test_calendar_day_view_without_date(self):
        """tests that the calendar for the day is not returned if no date is entered."""
        data = {"view": "day"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Не указана дата для вывода календаря."
        )

    def test_calendar_view_success(self):
        """Тестирует, что календарь на месяц возвращается."""
        data = {"view": "month", "month": "2025-06"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("month", response.data)

    def test_calendar_month_view_without_date(self):
        """Tests that the calendar for the month is being returned."""
        data = {"view": "month"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["error"], "Не указан месяц для вывода календаря."
        )

    def test_calendar_month_view_invalid_date(self):
        """Тестирует, что календарь на месяц не возвращается, если формат даты неверный."""
        data = {"view": "month", "month": "2025.06"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Неверный формат даты.")

    def test_calendar_default_day_view(self):
        """Tests that the calendar for the month is not returned if the date format is incorrect."""
        data = {"date": "2025-06-05"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tasks", response.data)

    def test_calendar_view_invalid_view(self):
        """Tests that the calendar is not returned if an incorrect parameter is entered: view."""
        data = {"view": "week", "month": "2025-06"}
        response = self.client.get(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["error"], "Введены неверные параметры.")