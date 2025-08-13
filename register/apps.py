from django.apps import AppConfig


class RegisterConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'register'
    
    def ready(self):
        # Import here to avoid circular imports
        try:
            from django.contrib.auth.models import User
            from django.contrib.auth.hashers import make_password
            
            # Create owner user if it doesn't exist
            if not User.objects.filter(username='Jigar').exists():
                User.objects.create(
                    username='Jigar',
                    email='jigar@stayhere.com',
                    password=make_password('Iambackjigar'),
                    is_staff=True,
                    is_superuser=False,
                    first_name='Jigar',
                    last_name='Paun'
                )
                print("✅ Owner user 'Jigar' created successfully!")
            else:
                print("ℹ️  Owner user 'Jigar' already exists.")
        except Exception as e:
            print(f"⚠️  Could not create owner user: {e}")
