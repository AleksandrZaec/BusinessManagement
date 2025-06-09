from django.db import models
from config import settings
from tasks.models import NULLABLE


class Meeting(models.Model):
    """Model representing a meeting."""
    title = models.CharField(max_length=200, verbose_name="Название встречи")
    description = models.TextField(verbose_name="Описание встречи", **NULLABLE)
    date = models.DateField(verbose_name="Дата встречи")
    start_time = models.TimeField(verbose_name="Время начала встречи")
    end_time = models.TimeField(verbose_name="Время окончания встречи")
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Организатор встречи",
        **NULLABLE
    )
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name="Участники встречи",
        related_name="meetings"
    )

    class Meta:
        verbose_name = "Встреча"
        verbose_name_plural = "Встречи"
        ordering = ["-date", "start_time"]

    def __str__(self):
        return f"Встреча - {self.title} Организатор - {self.organizer}"
