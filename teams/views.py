from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, RetrieveAPIView, UpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from teams.models import Team
from teams.serializers import TeamDetailSerializer, TeamSerializer
from users.permissions import IsAdminPermission


class TeamCreateAPIView(CreateAPIView):
    """Create a new Team instance. Admin only."""

    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated & IsAdminPermission,)


class TeamListAPIView(ListAPIView):
    """List all Team instances."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamRetrieveAPIView(RetrieveAPIView):
    """Retrieve a single Team instance by ID."""

    queryset = Team.objects.all()
    serializer_class = TeamDetailSerializer


class TeamUpdateAPIView(UpdateAPIView):
    """Update an existing Team instance. Admin only."""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = (IsAuthenticated & IsAdminPermission)


class TeamDestroyAPIView(DestroyAPIView):
    """Delete a Team instance. Admin only."""

    queryset = Team.objects.all()
    permission_classes = (IsAuthenticated & IsAdminPermission)
