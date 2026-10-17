from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = "Creates an initial superuser for the magazine platform."

    def add_arguments(self, parser):
        parser.add_argument('--email', default='admin@welcometonigeria.com')
        parser.add_argument('--password', default='adminpass1234')
        parser.add_argument('--name', default='Magazine Editor')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password']
        name = options['name']
        name_parts = name.split(' ', 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ''

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f"Superuser with email {email} already exists."))
            return

        user = User.objects.create_superuser(
            username='admin',
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            bio='Editor-in-chief, Welcome to Nigeria Travel Magazine.',
        )
        self.stdout.write(self.style.SUCCESS(f"Superuser successfully created: {email}"))

