import os
from pathlib import Path

# BASE DIRECTORY of the Django project
BASE_DIR = Path(__file__).resolve().parent.parent

# Custom directory paths
TEMPLATE_DIR = BASE_DIR / 'templates'
STATIC_DIR   = BASE_DIR / 'static'
STATIC_ROOT  = BASE_DIR / 'staticfiles'  # Used for collectstatic in production
MEDIA_ROOT   = BASE_DIR / 'media'        # Where uploaded files are stored

# SECURITY SETTINGS
SECRET_KEY = 'hpbv()ep00boce&o0w7z1h)st148(*m@6@-rk$nn)(n9ojj4c0'  # Replace before deployment
DEBUG = True  # ⚠️ Set to False in production
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# APPLICATIONS
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

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ROOT URL CONFIGURATION
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
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# DATABASE (SQLite for development)
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

# ✅ STATIC FILES
STATIC_URL = '/static/'
STATICFILES_DIRS = [STATIC_DIR]       # Local static (CSS, JS, etc.)
STATIC_ROOT = STATIC_ROOT             # Production static root for `collectstatic`

# ✅ MEDIA FILES
MEDIA_URL = '/media/'                 # URL prefix for media files
MEDIA_ROOT = MEDIA_ROOT              # Actual directory where uploaded files are stored

# LOGIN REDIRECT
LOGIN_REDIRECT_URL = '/afterlogin/'

# EMAIL SETTINGS (for notifications, password reset, etc.)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'from@gmail.com'          # ✅ Replace with sender email
EMAIL_HOST_PASSWORD = 'your_app_password'   # ✅ Use App Password for Gmail
EMAIL_RECEIVING_USER = ['to@gmail.com']     # ✅ Replace with target inbox

# DEFAULT AUTO FIELD
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
