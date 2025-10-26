import os
from pathlib import Path
import dj_database_url 

# BASE DIRECTORY of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Custom directory paths
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR   = BASE_DIR / 'static'
STATIC_ROOT  = BASE_DIR / 'staticfiles'  # Used for collectstatic in production
MEDIA_ROOT   = BASE_DIR / 'media'        # Where uploaded files are stored

# SECURITY SETTINGS
SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')  # ← use env on Render
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.onrender.com']

CSRF_TRUSTED_ORIGINS = ['https://*.onrender.com']
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# APPLICATIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'widget_tweaks',

    # Local apps
    'hospital',
]

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← add this
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# URL & WSGI
ROOT_URLCONF = 'hospitalmanagement.urls'
WSGI_APPLICATION = 'hospitalmanagement.wsgi.application'

# TEMPLATES
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],  # ✅ Custom templates directory
        'APP_DIRS': True,        # ✅ Enables looking inside app/templates folders
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # Required for auth views
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# DATABASE (SQLite - for development)
DATABASES = {
    'default': dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
    )
}


# PASSWORD VALIDATION
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNATIONALIZATION
LANGUAGE_CODE = 'en-gb'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC FILES
STATIC_URL = '/static/'
STATIC_DIR = BASE_DIR / 'static'
STATICFILES_DIRS = [STATIC_DIR] if STATIC_DIR.exists() else []
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

STORAGES = {
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    }
}


# AUTH REDIRECTS
LOGIN_URL = '/adminlogin/'
LOGIN_REDIRECT_URL = '/afterlogin/'    # After successful login
LOGOUT_REDIRECT_URL = '/'              # ✅ Redirect to home after logout

# EMAIL SETTINGS (For password reset, notifications, etc.)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'from@gmail.com'          # ✅ Replace with sender Gmail
EMAIL_HOST_PASSWORD = 'your_app_password'   # ✅ Use Gmail App Password
EMAIL_RECEIVING_USER = ['to@gmail.com']     # ✅ Replace with your receiving email

# DEFAULT FIELD TYPE
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
