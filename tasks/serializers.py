from rest_framework.serializers import ModelSerializer
from tasks.models import Comment, Task


class TaskSerializer(ModelSerializer):
    """Serializer for the Task model."""

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "author",
            "task_performer",
        )


class CommentSerializer(ModelSerializer):
    """Serializer for the Comment model."""

    class Meta:
        model = Comment
        fields = (
            "id",
            "text",
            "author",
            "task",
            "created_at",
        )


class TaskDetailSerializer(ModelSerializer):
    """Detailed serializer for the Task model."""
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Task
        fields = (
            "id",
            "title",
            "description",
            "status",
            "deadline",
            "author",
            "task_performer",
            "comments",
        )
