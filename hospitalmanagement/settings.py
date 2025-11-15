import os
from pathlib import Path
import dj_database_url

# ─────────────────────────────────────────────
# BASE DIRECTORY
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Directories
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'

# ─────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────

SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

# 🔧 TEMP: Force DEBUG=True so we can see full error page on Heroku.
# After fixing the 500 error, change this back to the env-based version:
# DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
DEBUG = True

# ✔ ALLOWED_HOSTS — LOCAL + HEROKU APPS
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'hospital-management-web.herokuapp.com',
    'hospital-management-web-4963f51d811d.herokuapp.com',
]

# ✔ CSRF Origins (MUST be full URLs)
CSRF_TRUSTED_ORIGINS = [
    'https://hospital-management-web.herokuapp.com',
    'https://hospital-management-web-4963f51d811d.herokuapp.com',
]

# ✔ Needed for Heroku reverse proxy
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# ─────────────────────────────────────────────
# APPLICATIONS
# ─────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party
    'widget_tweaks',

    # Local apps
    'hospital',
]

# ─────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # static files on Heroku
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hospitalmanagement.urls'
WSGI_APPLICATION = 'hospitalmanagement.wsgi.application'

# ─────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ─────────────────────────────────────────────
# DATABASE — SQLite local, PostgreSQL on Heroku
# ─────────────────────────────────────────────

DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}

# ─────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ─────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────

LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# STATIC & MEDIA FILES
# ─────────────────────────────────────────────

STATIC_URL = '/static/'

# Where STATICFILES_DIRS exists in development
STATICFILES_DIRS = [STATIC_DIR] if STATIC_DIR.exists() else []

# Where static files are collected for production (Heroku)
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_ROOT  # uses BASE_DIR / 'media' defined above

# WhiteNoise storage
STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    }
}

# ─────────────────────────────────────────────
# AUTH REDIRECTS
# ─────────────────────────────────────────────

LOGIN_URL = '/adminlogin/'
LOGIN_REDIRECT_URL = '/afterlogin/'
LOGOUT_REDIRECT_URL = '/'

# ─────────────────────────────────────────────
# EMAIL SETTINGS (Used for notifications)
# ─────────────────────────────────────────────

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'from@gmail.com'             # replace when needed
EMAIL_HOST_PASSWORD = 'your_app_password'      # replace with Gmail App Password
EMAIL_RECEIVING_USER = ['to@gmail.com']

# ─────────────────────────────────────────────
# DEFAULT FIELD TYPE
# ─────────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
