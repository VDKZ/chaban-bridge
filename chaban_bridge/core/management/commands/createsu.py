# Built-in
import os
from typing import Any

# Django
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandParser


class Command(BaseCommand):
    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--force-reset-password",
            dest="force_reset_password",
            default=False,
            action="store_true",
            help="Force the super user reset password even if already existing",
        )

    def handle(self, *args: Any, **options: Any) -> None:
        superuser_username = os.getenv("DJANGO_SUPERUSER_USERNAME")
        User = get_user_model()
        try:
            user = User.objects.get(username=superuser_username)
        except User.DoesNotExist:
            User.objects.create_superuser(
                superuser_username,
                os.getenv("DJANGO_SUPERUSER_EMAIL"),
                os.getenv("DJANGO_SUPERUSER_PASSWORD"),
            )
            print("Created super user as per env variables provided")
        else:
            if options["force_reset_password"]:
                admin_pwd = os.getenv("DJANGO_SUPERUSER_PASSWORD")
                if admin_pwd is not None and len(admin_pwd) >= 20:
                    user.set_password(admin_pwd)
                    user.save()
                    print(
                        "Super user already exist. Reset password as per instruction."
                    )
                else:
                    print(
                        "Super user password not reset as not provided or does not match requirements."
                    )
            else:
                print("Super user already exist. Did not create it.")
