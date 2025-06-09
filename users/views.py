from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from users.models import User
from users.serializers import UserSerializer


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


class UserDeleteAPIView(DestroyAPIView):
    """API view to delete an existing User."""
    queryset = User.objects.all()