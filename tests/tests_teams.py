from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from teams.models import Team
from users.models import User


class TeamTestCase(APITestCase):
    """Tests for the Team API."""

    def setUp(self):
        """Environment for the tests."""
        self.client_1 = APIClient()
        self.client_2 = APIClient()

        self.user_role = User.objects.create(email="user@test.test", role="user")
        self.admin_role = User.objects.create(email="admin@test.test", role="admin")

        self.client_1.force_authenticate(user=self.user_role)
        self.client_2.force_authenticate(user=self.admin_role)

        self.team = Team.objects.create(
            name="Test team",
            created_at=timezone.now(),
            team_admin=self.admin_role,
        )
        self.team.members.set([self.user_role, self.admin_role])

    def test_team_create(self):
        """Testing the creation of a new team."""
        url = reverse("team:create_team")
        data = {
            "name": "New team",
            "created_at": timezone.now(),
            "members": [self.user_role.pk, self.admin_role.pk],
        }

        response = self.client_1.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Team.objects.count(), 1)

        response = self.client_2.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.count(), 2)

    def test_team_retrieve(self):
        """Testing the viewing of a single command."""
        url = reverse("team:retrieve_team", args=(self.team.pk,))
        response = self.client_1.get(url)
        data = response.json()

        expected = [
            {
                "email": self.user_role.email,
                "id": self.user_role.pk,
                "is_active": self.user_role.is_active,
                "role": self.user_role.role,
            },
            {
                "email": self.admin_role.email,
                "id": self.admin_role.pk,
                "is_active": self.admin_role.is_active,
                "role": self.admin_role.role,
            },
        ]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), self.team.name)
        self.assertEqual(data.get("members"), expected)

    def test_team_update(self):
        """Testing the team's update."""
        url = reverse("team:update_team", args=(self.team.pk,))
        data = {"name": "Test team updated"}

        response = self.client_1.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.team.name, "Test team")

        response = self.client_2.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("name"), "Test team updated")

    def test_team_delete(self):
        """Testing the removal of the command."""
        url = reverse("team:destroy_team", args=(self.team.pk,))

        response = self.client_1.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Team.objects.count(), 1)

        response = self.client_2.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Team.objects.count(), 0)

    def test_team_list(self):
        """Testing the command list view."""
        url = reverse("team:teams_list")
        response = self.client_2.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(data), 1)
        self.assertEqual(type(data), list)
