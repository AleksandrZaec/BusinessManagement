from django.contrib import admin
from evaluations.models import Evaluation


@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
    """Class for configuring the display of the "Evaluation" model in the administrative panel."""

    list_display = (
        "pk",
        "task",
        "author",
        "score",
    )