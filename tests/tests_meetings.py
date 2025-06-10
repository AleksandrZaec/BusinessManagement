from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from meetings.models import Meeting
from users.models import User


class MeetingTestCase(APITestCase):
    """Tests for the Meeting API."""

    def setUp(self):
        """Environment for the tests."""
        self.user = User.objects.create(email="user@test.test", role="user")
        self.manager = User.objects.create(email="manager@test.test", role="manager")

        self.client.force_authenticate(user=self.user)

        self.meeting = Meeting.objects.create(
            title="Test meeting",
            date="2025-06-06",
            start_time="10:00:00",
            end_time="11:00:00",
            organizer=self.manager,
        )
        self.meeting.participants.set([self.user, self.manager])

        self.meeting_2 = Meeting.objects.create(
            title="Test meeting",
            date="2025-06-06",
            start_time="18:00:00",
            end_time="19:00:00",
            organizer=self.manager,
        )
        self.meeting_2.participants.set([self.manager])

    def test_meeting_create(self):
        """Testing the creation of a new meeting."""
        url = reverse("meeting:meeting-list")
        data = {
            "title": "New meeting",
            "date": "2025-06-06",
            "start_time": "13:00:00",
            "end_time": "14:00:00",
            "organizer": self.manager.pk,
            "participants": [self.user.pk, self.manager.pk],
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Meeting.objects.count(), 3)

    def test_invalid_time_meeting_create(self):
        """
        Testing the creation of a new meeting with a time intersection.
        Checking for the intersection of time and the end time of the meeting.
        """
        url = reverse("meeting:meeting-list")
        data_1 = {
            "title": "Time intersects",
            "date": "2025-06-06",
            "start_time": "10:00:00",
            "end_time": "10:30:00",
            "organizer": self.manager.pk,
            "participants": [self.user.pk, self.manager.pk],
        }
        data_2 = {
            "title": "End date is earlier than start date",
            "date": "2025-06-05",
            "start_time": "11:00:00",
            "end_time": "10:30:00",
            "organizer": self.manager.pk,
            "participants": [self.user.pk, self.manager.pk],
        }

        response_1 = self.client.post(url, data_1)
        response_2 = self.client.post(url, data_2)

        self.assertEqual(response_1.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Meeting.objects.count(), 2)

    def test_meeting_retrieve(self):
        """Testing the viewing of a single meeting."""
        url = reverse("meeting:meeting-detail", args=(self.meeting.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.meeting.title)

    def test_meeting_update(self):
        """Testing the appointment update."""
        url = reverse("meeting:meeting-detail", args=(self.meeting.pk,))
        data = {"start_time": "10:00:00", "end_time": "10:30:00"}

        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("end_time"), "10:30:00")

    def test_invalid_time_meeting_update(self):
        """Testing the time-lapse meeting update."""
        url = reverse("meeting:meeting-detail", args=(self.meeting.pk,))
        data = {"start_time": "18:00:00", "end_time": "18:30:00"}

        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.meeting.start_time, "10:00:00")

    def test_meeting_delete(self):
        """Testing the deletion of an appointment."""
        url = reverse("meeting:meeting-detail", args=(self.meeting.pk,))

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Meeting.objects.count(), 1)

    def test_meeting_list(self):
        """Testing the appointment list view."""
        url = reverse("meeting:meeting-list")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 2)

    def test_user_meeting_list(self):
        """Testing viewing the user's appointment list."""
        url = reverse("meeting:meeting-my-meetings")
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
