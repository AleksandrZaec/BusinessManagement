import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from dotenv import load_dotenv

load_dotenv()

User = get_user_model()


class Command(BaseCommand):
    """The command to create a superuser"""

    def handle(self, *args, **options):
        email = os.getenv('SUPERUSER_EMAIL')
        password = os.getenv('SUPERUSER_PASSWORD')

        user = User.objects.create(email=email)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.save()
