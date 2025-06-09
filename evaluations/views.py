from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from evaluations.models import Evaluation
from evaluations.serializers import EvaluationSerializer


class EvaluationViewSet(ModelViewSet):
    """A viewset for viewing, creating, updating, and deleting Evaluation instances."""
    queryset = Evaluation.objects.select_related("task", "author")
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            raise ValidationError("Оценка для этой задачи от данного пользователя уже существует.")
