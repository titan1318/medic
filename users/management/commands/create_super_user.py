import os
from datetime import date

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = ('Create a superuser with the specified email\n'
            'Usage: python manage.py create__super_user email=john@example.com '
            'first_name=John last_name=Doe password=secretword')
    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='SuperUser email address')
        parser.add_argument('first_name', type=str, help='SuperUser first name')
        parser.add_argument('last_name', type=str, help='SuperUser last name')
        parser.add_argument('password', type=str, help='SuperUser password')

    def handle(self, *args, **options):
        superuser_email = options['email']
        superuser_first_name = options['first_name']
        superuser_last_name = options['last_name']
        superuser_password = options['password']

        # Проверка наличия суперпользователя с таким email
        if User.objects.filter(email=superuser_email):
            self.stdout.write(self.style.ERROR(f'Superuser with email "{superuser_email}" already exists.'))
            return

        user = User.objects.create(
            email=superuser_email,
            first_name=superuser_first_name,
            last_name=superuser_last_name,
            is_superuser=True,
            is_staff=True,
            is_active=True
        )
        user.set_password(superuser_password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f'Superuser with email "{superuser_email}" successfully created.'))
