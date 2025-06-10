from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("user/", include("users.urls", namespace="user")),
    path("evaluation/", include("evaluations.urls", namespace="evaluation")),
    path("meeting/", include("meetings.urls", namespace="meeting")),
    path("task/", include("tasks.urls", namespace="task")),
    path("team/", include("teams.urls", namespace="team")),
    path("calendar/", include("calendars.urls", namespace="calendar")),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

