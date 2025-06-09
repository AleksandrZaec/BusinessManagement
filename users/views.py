from django.db.models import Avg
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from users.models import User
from users.serializers import UserSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from users.permissions import IsOwnerPermission
from rest_framework.response import Response
from django.utils.dateparse import parse_date
from evaluations.models import Evaluation


class UserCreateAPIView(CreateAPIView):
    """API view to create a new User."""
    serializer_class = UserSerializer


class UserListAPIView(ListAPIView):
    """API view to list all Users."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """API view to update an existing User."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated & IsAdminUser | IsOwnerPermission,)


class UserDeleteAPIView(DestroyAPIView):
    """API view to delete an existing User."""
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated & IsAdminUser | IsOwnerPermission,)


class UserAverageScoreView(RetrieveAPIView):
    """A view to get the average score of the user."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        start = parse_date(request.query_params.get("start"))
        end = parse_date(request.query_params.get("end"))

        evaluations = Evaluation.objects.filter(task__task_performer=user)

        if start:
            evaluations = evaluations.filter(created_at__gte=start)
        if end:
            evaluations = evaluations.filter(created_at__lte=end)

        avg_score = evaluations.aggregate(avg=Avg("score"))["avg"]

        return Response(
            {
                "user_id": user.id,
                "task_performer": user.email,
                "average_score": round(avg_score, 2) if avg_score else None,
                "period": {"start": start, "end": end},
            }
        )
