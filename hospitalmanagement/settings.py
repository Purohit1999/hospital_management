import os
from pathlib import Path

# BASE DIRECTORY of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Custom directory paths
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR   = BASE_DIR / 'static'
STATIC_ROOT  = BASE_DIR / 'staticfiles'
MEDIA_ROOT   = BASE_DIR / 'media'

# SECURITY SETTINGS
SECRET_KEY = 'hpbv()ep00boce&o0w7z1h)st148(*m@6@-rk$nn)(n9ojj4c0'  # Replace this for production
DEBUG = True  # Turn OFF in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # Add domain names for deployment

# APPLICATION DEFINITIONS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'widget_tweaks',  # Allows form customization in templates

    # Local apps
    'hospital',
]

# MIDDLEWARE DEFINITIONS
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# URL CONFIGURATION
ROOT_URLCONF = 'hospitalmanagement.urls'
WSGI_APPLICATION = 'hospitalmanagement.wsgi.application'

# TEMPLATES CONFIGURATION
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],  # ✅ Custom templates folder
        'APP_DIRS': True,        # ✅ Enables app-level templates too
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


# DATABASE CONFIGURATION (SQLite for development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

# STATIC & MEDIA FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]  # Development static files
STATIC_ROOT = STATIC_ROOT  # Where `collectstatic` places production files

MEDIA_URL = '/media/'
MEDIA_ROOT = MEDIA_ROOT  # Uploaded files storage

# LOGIN SETTINGS
LOGIN_REDIRECT_URL = '/afterlogin/'

# EMAIL SETTINGS
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'  # Correct backend class
EMAIL_HOST = 'smtp.gmail.com'  # Gmail SMTP server
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'from@gmail.com'       # Replace with your email
EMAIL_HOST_PASSWORD = 'your_app_password'  # Use App Password if using Gmail
EMAIL_RECEIVING_USER = ['to@gmail.com']

# DEFAULT PRIMARY KEY FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
