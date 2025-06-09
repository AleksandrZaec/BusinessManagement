from django.db import models
from config import settings
from tasks.models import NULLABLE


class Team(models.Model):
    """Team model for storing information about teams."""
    name = models.CharField(max_length=100, verbose_name="Team name")
    description = models.TextField(verbose_name="Team description", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    team_admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Team administrator",
        **NULLABLE,
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Team members",
        related_name="teams",
    )

    class Meta:
        verbose_name = "Команда"
        verbose_name_plural = "Команды"

    def __str__(self):
        return f"Team - {self.name} (Admin: {self.team_admin})"
