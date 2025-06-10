from rest_framework.serializers import ModelSerializer
from tasks.models import Comment, Task
from rest_framework import serializers


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
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

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
