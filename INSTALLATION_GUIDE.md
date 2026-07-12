# FINDLOST - Installation & Deployment Guide

## Overview

The FINDLOST Django application is designed to work in two modes:

1. **Standard Mode (with face recognition)**
   - Requires C++ build tools
   - Full facial detection and matching capabilities
   - Best for production on systems with build tools

2. **Lightweight Mode (without face recognition)**
   - No C++ compiler required
   - All core functionality available
   - Optimal for Codespaces and restricted environments

This guide covers both installation modes.

---

## Quick Start (Lightweight Mode - No C++ Required)

### Prerequisites
- Python 3.8+ (tested with 3.14.3)
- pip package manager

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/adityapatro495-lab/Find-Lostperson-relocator.git
cd Find-Lostperson-relocator/findlost_app

# 2. Install dependencies (without face recognition)
pip install -r requirements.txt

# 3. Create database
python manage.py migrate

# 4. Create admin user
python manage.py createsuperuser

# 5. Start development server
python manage.py runserver

# 6. Access the application
# Navigate to http://localhost:8000/
# Admin panel: http://localhost:8000/admin/
```

**Time to ready:** ~2 minutes

---

## Full Installation (with Face Recognition)

### Prerequisites

#### Windows
- Python 3.8-3.11 (NOT 3.14 - dlib doesn't support it yet)
- Visual Studio Build Tools with C++ support
- CMake 3.20+

Installation:
```bash
# Install Visual Studio Build Tools with C++
# Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/
# During installation, select "Desktop development with C++"

# Install CMake
pip install cmake
```

#### Linux (Ubuntu/Debian)
- Python 3.8-3.11
- C++ compiler and development tools
- CMake

Installation:
```bash
sudo apt update
sudo apt install build-essential cmake python3-dev python3-pip
```

#### macOS
- Python 3.8-3.11
- Xcode Command Line Tools
- CMake

Installation:
```bash
xcode-select --install
brew install cmake
```

### Installation Steps with Face Recognition

```bash
# 1. Clone repository
git clone https://github.com/adityapatro495-lab/Find-Lostperson-relocator.git
cd Find-Lostperson-relocator/findlost_app

# 2. Create virtual environment (optional but recommended)
python -m venv venv

# 3. Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 4. Update pip
pip install --upgrade pip

# 5. Install dependencies with face recognition
# FIRST uncomment these lines in requirements.txt:
# dlib==19.24.2
# face-recognition==1.3.0
# face-recognition-models==0.3.0

# Then install:
pip install -r requirements.txt

# This will take 10-15 minutes as dlib compiles from source

# 6. Verify installation
python -c "import face_recognition; print('✓ Face recognition installed')"

# 7. Run remaining setup
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

**Time to ready:** ~15 minutes (depends on dlib compilation)

---

## Environment Configuration

### Development (settings.py defaults)

```python
DEBUG = True
SECRET_KEY = 'django-insecure-...'  # Placeholder
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production Configuration

**Create `.env` file:**
```
SECRET_KEY=your-production-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@localhost:5432/findlost
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Update settings.py:**
```python
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

# Database configuration
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600
    )
}

# Email configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
```

**Install production dependencies:**
```bash
pip install python-decouple dj-database-url psycopg2-binary gunicorn whitenoise
```

---

## Deployment Options

### Option 1: Heroku (Recommended for Quick Start)

```bash
# 1. Install Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Create Procfile
echo "web: gunicorn findlost.wsgi" > Procfile

# 3. Create runtime.txt (specify Python 3.11)
echo "python-3.11.0" > runtime.txt

# 4. Push to Heroku
git add .
git commit -m "Prepare for Heroku deployment"
heroku create your-app-name
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
git push heroku main
heroku run python manage.py migrate
```

### Option 2: Digital Ocean (Full Control)

```bash
# 1. SSH into your server
ssh root@your.server.ip

# 2. Install dependencies
apt update && apt install -y python3.11 python3.11-venv python3-pip postgresql nginx supervisor

# 3. Clone repository
git clone https://github.com/your-repo/Find-Lostperson-relocator.git
cd Find-Lostperson-relocator/findlost_app

# 4. Create virtual environment
python3.11 -m venv venv
source venv/bin/activate

# 5. Install Python dependencies
pip install -r requirements.txt
pip install gunicorn python-decouple dj-database-url psycopg2-binary

# 6. Configure environment
nano .env  # Add configuration as shown above

# 7. Run migrations
python manage.py migrate
python manage.py collectstatic

# 8. Create systemd service
# See: https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/gunicorn/
```

### Option 3: Docker (Production Best Practice)

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application
COPY . .

# Create static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "findlost.wsgi:application"]
```

```bash
# Build and run
docker build -t findlost .
docker run -p 8000:8000 -e SECRET_KEY=your-key findlost
```

---

## Troubleshooting

### dlib Installation Fails

**Error:** `error: Microsoft Visual C++ 14.0 or greater is required`

**Solution:**
1. Install Visual Studio Build Tools
2. Select "Desktop development with C++"
3. Reinstall dlib: `pip install --no-cache-dir dlib`

### Database Migration Fails

**Error:** `django.db.utils.OperationalError: no such table`

**Solution:**
```bash
python manage.py migrate --run-syncdb
python manage.py migrate
```

### Static Files Not Loading

**Error:** 404 on CSS/JavaScript files

**Solution (Development):**
- Ensure `DEBUG = True` in settings.py
- Run `python manage.py collectstatic`

**Solution (Production):**
```bash
python manage.py collectstatic --noinput
# Configure nginx to serve static files from staticfiles/ directory
```

### Port 8000 Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or find and kill process using port 8000
lsof -i :8000
kill -9 <PID>
```

### Face Recognition Not Available

**Error:** `ModuleNotFoundError: No module named 'face_recognition'`

**Solution:**
- This is expected if you used lightweight installation
- Either install build tools and rerun pip, or
- Use the application in lightweight mode (face matching disabled)

---

## Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test matching

# Run with verbose output
python manage.py test -v 2

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

---

## Verification Checklist

After installation, verify:

```bash
# ✓ Django system checks
python manage.py check

# ✓ Migrations applied
python manage.py migrate

# ✓ Database accessible
python manage.py shell
>>> from accounts.models import UserProfile
>>> UserProfile.objects.count()
0

# ✓ Tests passing
python manage.py test

# ✓ Server starts
python manage.py runserver

# ✓ Face recognition available (optional)
python -c "import face_recognition; print('Available')" 2>/dev/null || echo "Not installed (expected for lightweight)"
```

---

## Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/deployment/checklist/)
- [face_recognition Library](https://github.com/ageitgey/face_recognition)
- [Gunicorn Documentation](https://gunicorn.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Django system checks: `python manage.py check`
3. Check application logs
4. Open an issue on GitHub with:
   - Python version
   - OS
   - Full error traceback
   - Steps to reproduce

---

**Last Updated:** July 12, 2026  
**Status:** Production Ready ✓
