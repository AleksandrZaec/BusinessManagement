from django.contrib import admin

from meetings.models import Meeting


@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    """Class for configuring the display of the "Meeting" model in the administrative panel."""

    list_display = (
        "pk",
        "title",
        "date",
        "organizer",
    )

    list_filter = (
        "date",
        "organizer",
    )