from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from rest_framework.permissions import AllowAny
from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserDeleteAPIView, UserListAPIView, UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path("register/", UserCreateAPIView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("users/", UserListAPIView.as_view(), name="users_list"),
    path("update/<int:pk>/", UserUpdateAPIView.as_view(), name="update_user"),
    path("delete/<int:pk>/", UserDeleteAPIView.as_view(), name="delete_user"),
    path("login/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)),name = "login"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
]
