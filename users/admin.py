from django.contrib import admin
from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Class for configuring the display of the "User" model in the administrative panel"""

    list_display = (
        "pk",
        "email",
    )