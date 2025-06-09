from django.urls import path
from teams.apps import TeamsConfig
from teams.views import (TeamCreateAPIView, TeamDestroyAPIView,
                         TeamListAPIView, TeamRetrieveAPIView,
                         TeamUpdateAPIView)

app_name = TeamsConfig.name

urlpatterns = [
    path("create/", TeamCreateAPIView.as_view(), name="create_team"),
    path("teams/", TeamListAPIView.as_view(), name="teams_list"),
    path("retrieve/<int:pk>/", TeamRetrieveAPIView.as_view(), name="retrieve_team"),
    path("update/<int:pk>/", TeamUpdateAPIView.as_view(), name="update_team"),
    path("destroy/<int:pk>/", TeamDestroyAPIView.as_view(), name="destroy_team"),
]
