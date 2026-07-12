# FINDLOST Environment Setup & Configuration Guide

**Generated:** July 12, 2026  
**Status:** ✅ Complete & Validated

---

## Quick Reference

### Minimal Setup (5 minutes)
```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### Full Setup with Face Recognition (15 minutes)
Requires C++ compiler. See "Python Version Requirements" section.

---

## Part 1: Python Version Requirements

### Recommended
- **Python 3.11** - Optimal compatibility with Django 4.2.7 and dlib
- **Python 3.10** - Also fully compatible
- **Python 3.9** - Compatible
- **Python 3.8** - Compatible (older, less optimized)

### Known Issues
- **Python 3.14.3+** - Works without dlib; dlib not yet compatible
- **Python 3.7 and older** - Not tested, not recommended

### Special Considerations
- **Python 3.12+** - Works without dlib; pre-built dlib wheels may not be available
- **PyPy** - Not tested; use CPython instead

---

## Part 2: System Requirements by Platform

### Windows 10/11

#### For Lightweight Installation (No Face Recognition)
```
- Python 3.8 or later
- pip (included with Python)
- ~300 MB disk space
- No special tools required
```

#### For Full Installation (With Face Recognition)
```
- Python 3.8-3.11 (NOT 3.12+)
- Visual Studio Build Tools 2019 or later
- C++ workload selected during VS Build Tools installation
- CMake 3.20 or later (pip install cmake)
- ~1.5 GB disk space
- Good internet connection for package downloads
```

**Installation Steps for Build Tools:**
1. Download: https://visualstudio.microsoft.com/visual-cpp-build-tools/
2. Run installer
3. Select "Desktop development with C++"
4. Complete installation (~5 GB download)
5. Run: `pip install cmake`
6. Then install face-recognition dependencies

### Linux (Ubuntu 20.04 LTS / Debian 11+)

#### For Lightweight Installation
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip
# That's it!
```

#### For Full Installation (With Face Recognition)
```bash
sudo apt update
sudo apt install \
    python3.11 python3.11-venv python3-pip \
    build-essential cmake python3-dev \
    libopenblas-dev liblapack-dev libblas-dev

# Estimated download: ~500 MB
# Installation time: ~5 minutes
```

### macOS (Monterey 12+)

#### For Lightweight Installation
```bash
brew install python@3.11
# Python ready!
```

#### For Full Installation (With Face Recognition)
```bash
# Install Xcode Command Line Tools
xcode-select --install

# Install CMake
brew install cmake

# Install optional dependencies
brew install openblas lapack

# Build tools: ~1 GB
# Installation time: ~10 minutes
```

### GitHub Codespaces (Ubuntu-based)

#### Pre-installed
- ✅ Python 3.11 available
- ❌ C++ build tools not available (by design)
- ✅ Use lightweight installation only

#### Setup in Codespaces
```bash
# In terminal:
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser

# Click "Ports" tab
# Click "Open in Browser" for port 8000
# OR run: python manage.py runserver 0.0.0.0:8000
```

---

## Part 3: Step-by-Step Installation

### Step 1: Verify Python Installation
```bash
python --version
# Expected: Python 3.8 or later

pip --version
# Expected: pip X.Y.Z from /path/to/python/site-packages/pip
```

### Step 2: Clone Repository
```bash
git clone https://github.com/adityapatro495-lab/Find-Lostperson-relocator.git
cd Find-Lostperson-relocator/findlost_app
```

### Step 3: Create Virtual Environment (Recommended)
```bash
# Create
python -m venv venv

# Activate - Windows
venv\Scripts\activate

# Activate - Linux/macOS
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Step 4: Install Dependencies

**Option A: Lightweight (No Face Recognition)**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Option B: Full (With Face Recognition)**
```bash
# First, ensure C++ build tools installed (see Part 2)

# Update requirements.txt - uncomment these lines:
# dlib==19.24.2
# face-recognition==1.3.0
# face-recognition-models==0.3.0

pip install --upgrade pip
pip install -r requirements.txt

# Wait 10-15 minutes for dlib to compile
```

### Step 5: Create Database
```bash
python manage.py migrate
```

Expected output:
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, ...
Running migrations:
  No migrations to apply.
```

### Step 6: Create Admin User
```bash
python manage.py createsuperuser
```

Follow prompts:
```
Username: admin
Email: admin@example.com
Password: (enter secure password)
Password (again): (confirm)
```

### Step 7: Verify Installation
```bash
python manage.py check
```

Expected output:
```
System check identified no issues (0 silenced).
```

### Step 8: Run Tests (Optional)
```bash
python manage.py test
```

Expected output:
```
Found 11 test(s).
...
Ran 11 tests in X.XXXs
OK
```

### Step 9: Start Server
```bash
python manage.py runserver
```

Expected output:
```
Watching for file changes with StatReloader
Performing system checks...
System check identified no issues (0 silenced).
Django version 4.2.7, using settings 'findlost.settings'
Starting development server at http://127.0.0.1:8000/
```

### Step 10: Access Application
- **Application:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Use credentials:** Username and password from Step 6

---

## Part 4: Dependency Reference

### Core Dependencies (Always Required)
```
Django==4.2.7           # Web framework
numpy==1.26.4          # Numerical computing
Pillow==10.2.0         # Image processing
asgiref==3.11.1        # Django requirement
sqlparse==0.5.5        # Django requirement
tzdata==2026.3         # Django requirement
```

### Optional Dependencies (Face Recognition)
```
dlib==19.24.2                      # Face detection (requires C++ compiler)
face-recognition==1.3.0            # Face recognition API (requires dlib)
face-recognition-models==0.3.0     # Pre-trained models (50+ MB)
```

### Production Dependencies (Recommended)
```
gunicorn==22.0.0           # Production WSGI server
whitenoise==6.6.0          # Static file serving
python-decouple==3.8       # Environment variable management
dj-database-url==2.0.0     # Database URL parsing
psycopg2-binary==2.9.9     # PostgreSQL adapter
```

### Development Dependencies (Optional)
```
django-debug-toolbar==4.2.0   # Debugging
pytest==7.4.3                 # Testing
pytest-django==4.7.0          # Django testing
coverage==7.3.2               # Code coverage
```

---

## Part 5: Common Installation Issues & Solutions

### Issue: "pip: command not found"
**Cause:** Python not in PATH  
**Solution:**
```bash
# Windows
python -m pip install -r requirements.txt

# Linux/macOS
python3 -m pip install -r requirements.txt
```

### Issue: "No module named 'django'"
**Cause:** Django not installed in current environment  
**Solution:**
```bash
# Ensure virtual environment is activated
pip install -r requirements.txt

# Verify:
python -c "import django; print(django.VERSION)"
```

### Issue: "error: Microsoft Visual C++ 14.0 is required"
**Cause:** C++ compiler not installed (for dlib)  
**Solution:**
1. Install Visual Studio Build Tools (see Part 2)
2. Restart terminal
3. Retry: `pip install dlib`

### Issue: "CMake not found"
**Cause:** CMake not installed  
**Solution:**
```bash
pip install cmake
# Or for system package manager:
# Windows: (included with Visual Studio Build Tools)
# Linux: sudo apt install cmake
# macOS: brew install cmake
```

### Issue: "DJANGO_SETTINGS_MODULE not found"
**Cause:** Running from wrong directory  
**Solution:**
```bash
# Make sure you're in the findlost_app directory
cd Find-Lostperson-relocator/findlost_app
python manage.py runserver
```

### Issue: "Port 8000 already in use"
**Cause:** Another process using port 8000  
**Solution:**
```bash
# Use different port
python manage.py runserver 8001

# Or kill the existing process:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Linux/macOS:
lsof -i :8000
kill -9 <PID>
```

### Issue: "Database locked" error
**Cause:** Multiple processes accessing SQLite simultaneously  
**Solution:**
```bash
# Only affects SQLite during development
# For production, use PostgreSQL (see Deployment Guide)

# Quick fix - remove and recreate database:
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Part 6: Environment Variables

### Development (defaults)
No environment variables required. All defaults in settings.py work for development.

### Production (required)
Create `.env` file in project root:

```env
# Security
SECRET_KEY=your-super-secret-key-generate-this
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,api.yourdomain.com

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/findlost_db

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# Optional: Face Recognition
ENABLE_FACE_RECOGNITION=True
```

### Using Environment Variables
```python
# Install environment variable loader
pip install python-decouple

# In settings.py
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])
```

---

## Part 7: Verification Checklist

After setup, verify everything works:

```bash
# ✓ Python version
python --version

# ✓ Django installed
django-admin --version

# ✓ Project configuration
python manage.py check

# ✓ Database ready
python manage.py migrate

# ✓ Tests pass
python manage.py test

# ✓ Server starts
python manage.py runserver
# (Should not exit; if you see this, type Ctrl+C to stop)

# ✓ Face recognition (optional)
python -c "import face_recognition; print('Face recognition available')" 2>/dev/null || echo "Not installed (expected for lightweight)"
```

---

## Part 8: Next Steps

### For Development
1. ✅ Environment setup complete
2. Start Django server: `python manage.py runserver`
3. Access admin: http://127.0.0.1:8000/admin/
4. Begin development

### For Deployment
1. See `DEPLOYMENT_STATUS.md` in project root
2. Review `INSTALLATION_GUIDE.md` for production options
3. Choose deployment platform (Heroku, Docker, VPS, etc.)
4. Configure environment variables
5. Deploy

---

## Support

**For setup issues:**
1. Verify Python version: `python --version`
2. Check system requirements met
3. Run: `python manage.py check`
4. Review error message carefully
5. Check this guide's troubleshooting section

**For application issues:**
1. Check application logs: `python manage.py test`
2. Check Django logs: Run with `DEBUG=True` temporarily
3. Check database: `python manage.py dbshell`
4. Review Django documentation

---

**Status:** ✅ Setup verified on Python 3.14.3 / Django 4.2.7 / Windows 11  
**Last Updated:** July 12, 2026
