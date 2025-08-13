# Owner Account Setup Guide

## Problem
The owner login is showing "Invalid credentials or not an owner" error because no owner user exists in the database.

## Solution

### Option 1: Using Django Management Command (Recommended)

1. **Run the management command to create an owner user:**

```bash
python manage.py create_owner --username owner --password your_secure_password --email owner@stayhere.com
```

**Default credentials (if no arguments provided):**
- Username: `owner`
- Password: `owner123`
- Email: `owner@stayhere.com`

### Option 2: Using Django Admin

1. **Create a superuser first:**
```bash
python manage.py createsuperuser
```

2. **Login to Django Admin** at `https://your-domain.com/admin/`

3. **Create a new user:**
   - Go to "Users" section
   - Click "Add User"
   - Fill in the details:
     - Username: `owner` (or your preferred username)
     - Password: `your_secure_password`
     - Email: `owner@stayhere.com`
   - **IMPORTANT:** Check the "Staff status" checkbox
   - Save the user

### Option 3: Using Django Shell

1. **Open Django shell:**
```bash
python manage.py shell
```

2. **Run these commands:**
```python
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create owner user
user = User.objects.create(
    username='owner',
    email='owner@stayhere.com',
    password=make_password('your_secure_password'),
    is_staff=True,
    is_superuser=False,
    first_name='Stay Here',
    last_name='Owner'
)
print(f"Owner user created: {user.username}")
```

## Testing the Login

1. Go to the owner login page: `https://your-domain.com/owner/login/`
2. Use the credentials you created above
3. You should now be able to login successfully

## Security Notes

- **Change the default password** after first login
- Use a strong, unique password
- Consider enabling two-factor authentication for production
- Regularly update the password

## Troubleshooting

If you still get authentication errors:

1. **Check if the user exists:**
```bash
python manage.py shell
```
```python
from django.contrib.auth.models import User
User.objects.filter(username='owner').exists()
```

2. **Check if user is staff:**
```python
user = User.objects.get(username='owner')
print(f"Is staff: {user.is_staff}")
```

3. **Reset user password:**
```python
user.set_password('new_password')
user.save()
```

## For Production Deployment

Make sure to:
1. Use environment variables for sensitive data
2. Set up proper database backups
3. Use HTTPS in production
4. Regularly update Django and dependencies
