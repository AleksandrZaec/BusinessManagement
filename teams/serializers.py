from rest_framework.serializers import ModelSerializer
from teams.models import Team
from users.serializers import MemberSerializer


class TeamSerializer(ModelSerializer):
    """Serializer for Team model used for create and update operations."""

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "team_admin",
            "members",
        )


class TeamDetailSerializer(ModelSerializer):
    """Serializer for detailed view of a Team instance."""

    team_admin = MemberSerializer(read_only=True)
    members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = (
            "id",
            "name",
            "description",
            "created_at",
            "team_admin",
            "members",
        )