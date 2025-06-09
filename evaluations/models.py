from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from config import settings
from tasks.models import NULLABLE


class Evaluation(models.Model):
    """Model representing a task evaluation."""
    SCORE_CHOICES = [(i, str(i)) for i in range(1, 6)]
    task = models.ForeignKey(
        "tasks.Task",
        on_delete=models.CASCADE,
        verbose_name="Задача, к которой относится оценка",
        related_name="evaluations",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        verbose_name="Автор оценки",
        related_name="given_evaluations",
        **NULLABLE,
    )
    score = models.PositiveIntegerField(
        choices=SCORE_CHOICES,
        verbose_name="Оценка",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    comment = models.TextField(verbose_name="Комментарий к оценке", **NULLABLE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    @property
    def evaluated_user(self):
        return self.task.task_performer

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["task", "author"], name="unique_evaluation_per_task")
        ]

    def __str__(self):
        return f"Оценка от {self.author} - {self.score} за задачу '{self.task}'"
