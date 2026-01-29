from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Create initial admin user (temporary)"

    def handle(self, *args, **options):
        User = get_user_model()

        username = "rick"
        email = "ngor@myumanitoba.ca"
        password = "TempPassword123!"   # CHANGE AFTER LOGIN

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING("Admin user already exists"))
        else:
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS("Admin user created successfully"))
