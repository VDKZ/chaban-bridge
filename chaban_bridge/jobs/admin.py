# Django
from django.contrib import admin

# Local
from .models import Execution, Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ("organization", "name", "type", "frequency")


@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    model = Execution
    list_display = ("id", "job", "status", "created_at")
