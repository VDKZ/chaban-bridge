# Built-in
from typing import Any

# Django
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.fields.related import ForeignKey


class User(AbstractUser):
    profile: "Profile"

    def save(self, *args: Any, **kwargs: Any) -> None:
        created = self.pk is None
        super().save(*args, **kwargs)
        if created:
            Profile.objects.create(user=self)


class Organization(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        primary_key=True,
    )
    organization = ForeignKey(
        Organization, null=True, on_delete=models.CASCADE, related_name="profiles"
    )
