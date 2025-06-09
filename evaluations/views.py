from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from evaluations.models import Evaluation
from evaluations.serializers import EvaluationSerializer
from users.permissions import IsAuthorOrAdminForUpdateDelete


class EvaluationViewSet(ModelViewSet):
    """A viewset for viewing, creating, updating, and deleting Evaluation instances."""
    serializer_class = EvaluationSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrAdminForUpdateDelete]

    def get_queryset(self):
        qs = Evaluation.objects.select_related("task", "author")
        if self.request.user.is_staff:
            return qs
        return qs.filter(author=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            raise ValidationError("Оценка для этой задачи от данного пользователя уже существует.")
