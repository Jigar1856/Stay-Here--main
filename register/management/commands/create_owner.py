from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create an owner user for the Stay Here Snooker Club'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='owner', help='Username for the owner')
        parser.add_argument('--password', type=str, default='owner123', help='Password for the owner')
        parser.add_argument('--email', type=str, default='owner@stayhere.com', help='Email for the owner')

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']
        email = options['email']
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Use different credentials or update existing user.')
            )
            return
        
        # Create the owner user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_staff=True,
            is_superuser=False,
            first_name='Stay Here',
            last_name='Owner'
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created owner user:\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'Email: {email}\n'
                f'Staff Status: {user.is_staff}\n'
                f'Superuser Status: {user.is_superuser}'
            )
        )
        
        self.stdout.write(
            self.style.WARNING(
                '\n⚠️  IMPORTANT: Please change the default password after first login for security!'
            )
        )
