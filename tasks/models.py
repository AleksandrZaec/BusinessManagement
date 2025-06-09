from django.db import models

from config import settings

NULLABLE = {"blank": True, "null": True}


class TaskStatus(models.TextChoices):
    OPEN = "open", "Open"
    IN_PROGRESS = "in_progress", "In Progress"
    COMPLETED = "completed", "Completed"


class Task(models.Model):
    """Model representing a task within the system."""
    title = models.CharField(max_length=100, verbose_name="Название задачи")
    description = models.TextField(verbose_name="Описание задачи")
    status = models.CharField(
        max_length=20,
        choices=TaskStatus.choices,
        default=TaskStatus.OPEN,
        verbose_name="Статус задачи",
    )
    deadline = models.DateField(verbose_name="Дедлайн")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_tasks",
        verbose_name="Пользователь, который создал задачу",
        **NULLABLE,
    )
    task_performer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="performer_tasks",
        verbose_name="Исполнитель, которому назначена задача",
        **NULLABLE,
    )

    class Meta:
        verbose_name = "Задача"
        verbose_name_plural = "Задачи"

    def __str__(self):
        """
        Returns a string representation of the task instance.
        """
        return self.title


class Comment(models.Model):
    """Model representing a comment on a task."""
    text = models.TextField(verbose_name="Текст комментария")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Автор комментария",
        **NULLABLE,
    )
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name="Задача, к которой относится комментарий",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
        ordering = ["-created_at"]

    def __str__(self):
        """Returns a string representation of the comment instance."""
        return f"Комментарий от {self.author} - {self.created_at}"
