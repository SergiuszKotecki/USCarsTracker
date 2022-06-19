from django.contrib.auth.models import AbstractUser

from django.db import models


class CustomUser(AbstractUser):
    premium = models.BooleanField(default=False, help_text="Is user premium?")
