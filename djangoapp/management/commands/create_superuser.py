import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create a default superuser'

    def handle(self, *args, **kwargs):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'default_username')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'default_email@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'default_password')

        if not User.objects.filter(username=username).exists():
            User.objects.create_superuser(username, email, password)
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {username}'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
