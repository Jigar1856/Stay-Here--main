from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Setup owner user for Stay Here Snooker Club'

    def handle(self, *args, **options):
        username = 'Jigar'
        password = 'Iambackjigar'
        email = 'jigar@stayhere.com'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists.')
            )
            return
        
        # Create the owner user
        user = User.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            is_staff=True,
            is_superuser=False,
            first_name='Jigar',
            last_name='Paun'
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Successfully created owner user:\n'
                f'Username: {username}\n'
                f'Password: {password}\n'
                f'Email: {email}\n'
                f'Staff Status: {user.is_staff}\n'
                f'Superuser Status: {user.is_superuser}'
            )
        )
        
        self.stdout.write(
            self.style.SUCCESS(
                '\n🎉 You can now login at: https://stay-here-ly6z.onrender.com/owner/login/'
            )
        )
