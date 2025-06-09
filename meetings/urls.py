from rest_framework.routers import DefaultRouter
from meetings.apps import MeetingsConfig
from meetings.views import MeetingViewSet
from django.urls import path, include


app_name = MeetingsConfig.name
router = DefaultRouter()
router.register(r'', MeetingViewSet, basename='meeting')

urlpatterns = [
    path('', include(router.urls)),
]
