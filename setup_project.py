import os
import subprocess
import sys
from pathlib import Path


def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        sys.exit(1)


def setup_project():
    print("Starting project setup...")

    # Create virtual environment
    print("Creating virtual environment...")
    run_command("python -m venv venv")

    # Activate virtual environment
    print("Activating virtual environment...")
    if sys.platform == "win32":
        python_path = ".\\venv\\Scripts\\python"
        pip_path = ".\\venv\\Scripts\\pip"
    else:
        python_path = "./venv/bin/python"
        pip_path = "./venv/bin/pip"

    # Upgrade pip
    run_command(f"{python_path} -m pip install --upgrade pip")

    # Install core requirements first
    print("Installing Django and core packages...")
    run_command(f"{pip_path} install django python-dotenv")

    # Create Django project if it doesn't exist
    if not os.path.exists("school_project"):
        print("Creating Django project...")
        run_command(f"{python_path} -m django startproject school_project .")

    # Create apps if they don't exist
    if not os.path.exists("school"):
        print("Creating school app...")
        run_command(f"{python_path} manage.py startapp school")

    if not os.path.exists("accounts"):
        print("Creating accounts app...")
        run_command(f"{python_path} manage.py startapp accounts")

    # Install all other requirements
    print("Installing additional packages...")
    requirements = [
        "django-crispy-forms",
        "django-widget-tweaks",
        "django-bootstrap5",
        "djangorestframework",
        "drf-yasg",
        "Pillow",
        "django-storages",
        "django-allauth",
        "django-oauth-toolkit",
        "psycopg2-binary",
        "redis",
        "django-redis",
        "celery",
        "django-debug-toolbar",
        "django-extensions",
    ]

    for req in requirements:
        print(f"Installing {req}...")
        run_command(f"{pip_path} install {req}")

    # Create requirements.txt
    run_command(f"{pip_path} freeze > requirements.txt")

    # Update settings.py
    print("Updating settings.py...")
    settings_path = "school_project/settings.py"
    with open(settings_path, 'r') as f:
        settings_content = f.read()

    if 'INSTALLED_APPS = [' in settings_content:
        settings_updates = """
# Update INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Local apps
    'school.apps.SchoolConfig',
    'accounts.apps.AccountsConfig',

    # Third-party apps
    'rest_framework',
    'drf_yasg',
    'crispy_forms',
    'widget_tweaks',
    'django_bootstrap5',
    'debug_toolbar',
    'django_extensions',
    'storages',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'oauth2_provider',
]

# Middleware configuration
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Debug Toolbar
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Crispy Forms
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}

# Debug Toolbar
INTERNAL_IPS = [
    '127.0.0.1',
]

# Authentication settings
AUTH_USER_MODEL = 'accounts.User'
LOGIN_URL = 'account_login'
LOGIN_REDIRECT_URL = 'school:home'
LOGOUT_REDIRECT_URL = 'account_login'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# AllAuth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'

# Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email settings (update in .env)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 587)
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', True)
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

# Cache settings
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/1'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Celery settings
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'
"""
        with open(settings_path, 'w') as f:
            f.write(settings_updates)

    # Create necessary directories
    print("Creating project directories...")
    directories = [
        'media',
        'static',
        'templates/school',
        'templates/accounts',
        'templates/api',
    ]
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

    # Create .env file
    print("Creating .env file...")
    env_content = """
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:password@localhost:5432/school_db
REDIS_URL=redis://localhost:6379/1
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
"""
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(env_content)

    print("\nSetup completed successfully!")
    print("\nNext steps:")
    print("1. Update .env file with your actual credentials")
    print("2. Install and start Redis server")
    print("3. Create a PostgreSQL database")
    print("4. Run 'python manage.py makemigrations'")
    print("5. Run 'python manage.py migrate'")
    print("6. Run 'python manage.py createsuperuser'")
    print("7. Start the development server: 'python manage.py runserver'")


if __name__ == "__main__":
    setup_project()