from django.contrib import admin

from tasks.models import Comment, Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Class for configuring the display of the "Task" model in the administrative panel."""

    list_display = (
        "pk",
        "title",
        "status",
        "deadline",
        "task_performer",
    )

    list_filter = (
        "status",
        "deadline",
        "task_performer",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Class for configuring the display of the "Comment" model in the administrative panel."""

    list_display = (
        "pk",
        "text",
        "author",
        "task",
    )
