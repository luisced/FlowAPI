import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a default superuser'

    def handle(self, *args, **kwargs):
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL',
                               'default_email@example.com')
        username = os.environ.get(
            'DJANGO_SUPERUSER_USERNAME', 'default_username')
        name = os.environ.get('DJANGO_SUPERUSER_NAME',
                              'Default Name')  # Include name
        password = os.environ.get(
            'DJANGO_SUPERUSER_PASSWORD', 'default_password')

        # Check if a superuser with the given email already exists
        if not User.objects.filter(email=email).exists():
            # Adjust the order and parameters to match your custom User model
            User.objects.create_superuser(
                email=email, username=username, name=name, password=password)
            self.stdout.write(self.style.SUCCESS(
                f'Successfully created superuser: {email}'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists'))
