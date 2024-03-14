# Django
from django.db.models import DateTimeField, Model


class LifeCycleModel(Model):
    """Model mixin that provides lifecycle fields for creation and update."""

    created_at = DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        abstract = True
