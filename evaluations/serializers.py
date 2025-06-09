from rest_framework.serializers import ModelSerializer, StringRelatedField, PrimaryKeyRelatedField
from evaluations.models import Evaluation
from tasks.models import Task


class EvaluationSerializer(ModelSerializer):
    """Serializer for the Evaluation model."""
    task_performer = StringRelatedField(source="task.task_performer", read_only=True)
    task = PrimaryKeyRelatedField(queryset=Task.objects.all())

    class Meta:
        model = Evaluation
        fields = (
            "id",
            "task",
            "author",
            "score",
            "comment",
            "created_at",
            "task_performer",
        )
        read_only_fields = ("task_performer", "author")
