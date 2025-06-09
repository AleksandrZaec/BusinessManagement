from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from tasks.models import Task, Comment
from tasks.serializers import TaskSerializer, TaskDetailSerializer, CommentSerializer
from users.permissions import IsManagerPermission


class TaskViewSet(ModelViewSet):
    """ViewSet for handling Task operations."""

    queryset = Task.objects.all()

    def get_serializer_class(self):
        """Use detail serializer for retrieve action."""
        if self.action == "retrieve":
            return TaskDetailSerializer
        return TaskSerializer

    def get_permissions(self):
        """Set custom permissions per action."""
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAuthenticated(), IsManagerPermission()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Automatically assign the author when creating a task."""
        serializer.save(author=self.request.user)


class CommentViewSet(ModelViewSet):
    """ViewSet for handling Comment operations."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_permissions(self):
        """All actions require authenticated user."""
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        """Automatically assign the author when creating a comment."""
        serializer.save(author=self.request.user)