# Snooker Tournament Registration - Django Web App

## Features
- Player registration with payment (UPI/Net banking, QR Pay)
- Owner/admin login and dashboard
- Animated, modern frontend (CSS/JS)
- Payment screenshot upload for QR pay
- SQLite database (default)
- Ready for Render deployment

## Setup Instructions

1. **Clone/download the project**

2. **Install dependencies**
```
pip install -r requirements.txt
```

3. **Apply migrations**
```
python manage.py migrate
```

4. **Create superuser (for owner login)**
```
python manage.py createsuperuser
```

5. **Collect static files (for deployment)**
```
python manage.py collectstatic
```

6. **Run locally**
```
python manage.py runserver
```

7. **Access the app**
- Registration: http://localhost:8000/
- Owner login: http://localhost:8000/owner/login/
- Admin: http://localhost:8000/admin/

8. **Render Deployment**
- Create a Web Service on Render and connect your repo. Use these settings:
  - Root Directory: `reg`
  - Build Command: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
  - Start Command: `gunicorn reg.wsgi:application`
  - Environment Variables:
    - `SECRET_KEY`: a secure random string
    - `DEBUG`: `False`
    - `ALLOWED_HOSTS`: `.onrender.com,localhost,127.0.0.1`
    - (Optional) `DATABASE_URL` if you attach a Render PostgreSQL instance

## Sample Credentials
- **Owner/Admin:** Use the superuser you create in step 4
- **Test Player:** Register via the form

## Notes
- Place your QR code JPG at `register/static/register/img/qr_code.jpg`
- For demo, UPI/Net banking payment is always marked as successful
- For QR pay, upload a screenshot (manual verification)
- All static and media files are ready for Render

---

**No EJS files are used. All frontend is Django templates.**
