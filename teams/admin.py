from django.contrib import admin
from teams.models import Team


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Class for configuring the display of the "Team" model in the administrative panel."""

    list_display = (
        "pk",
        "name",
        "team_admin",
    )