from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from evaluations.models import Evaluation
from evaluations.serializers import EvaluationSerializer
from users.permissions import IsManagerPermission, IsAuthorOrAdminForUpdateDelete


class EvaluationViewSet(ModelViewSet):
    """A viewset for viewing, creating, updating, and deleting Evaluation instances."""
    serializer_class = EvaluationSerializer

    def get_queryset(self):
        return Evaluation.objects.select_related("task", "author")

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        permissions_list = [IsAuthenticated(), IsAuthorOrAdminForUpdateDelete()]
        if self.request.method != 'DELETE':
            permissions_list.insert(1, IsManagerPermission())
        return permissions_list

    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except IntegrityError:
            raise ValidationError("Оценка для этой задачи от данного пользователя уже существует.")
