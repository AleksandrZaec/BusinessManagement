from django.urls import path

from calendars.apps import CalendarsConfig
from calendars.views import CalendarAPIView

app_name = CalendarsConfig.name

urlpatterns = [
    path("calendar/", CalendarAPIView.as_view(), name="calendar"),
]