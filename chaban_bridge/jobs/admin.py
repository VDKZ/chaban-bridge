# Django
from django.contrib import admin

# Local
from .models import Execution, Job


# TODO remove that before prod
# can be usefull in initial test phase
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    model = Job
    list_display = ("name", "type", "frequency")


@admin.register(Execution)
class ExecutionAdmin(admin.ModelAdmin):
    model = Execution
    list_display = ("id", "job", "status", "created_at")
