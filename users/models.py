from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.TextChoices):
    USER = "user", "User"
    MANAGER = "manager", "Manager"
    ADMIN = "admin", "Admin"


class User(AbstractUser):
    """User model for storing information about users."""

    username = None
    email = models.EmailField(unique=True, verbose_name="Электронная почта пользователя (email)")
    first_name = models.CharField(max_length=50, verbose_name="Имя пользователя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия пользователя")
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.USER, verbose_name="User role")
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        """Returns the string representation of the object."""
        return f"{self.email} - {self.role}"
