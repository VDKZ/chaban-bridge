# Third-party
from user.models import Organization, Profile

# Django
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 0


@admin.register(get_user_model())
class UserModelAdmin(UserAdmin):
    # List
    list_display = [
        "username",
        "email",
        "first_name",
        "last_name",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    inlines = [*UserAdmin.inlines, ProfileInline]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ("id", "name")
