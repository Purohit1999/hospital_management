import os
from pathlib import Path
import dj_database_url
import stripe

# ─────────────────────────────────────────────
# BASE DIRECTORY
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# Directories
TEMPLATE_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"
MEDIA_DIR = BASE_DIR / "media"

# ─────────────────────────────────────────────
# SECURITY
# ─────────────────────────────────────────────

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")

# Use environment variable to control DEBUG
# Default = True for local dev. On Heroku set DEBUG=false in Config Vars.
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# ✔ ALLOWED_HOSTS — LOCAL + HEROKU APPS
ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv("ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")
    if host.strip()
]
ALLOWED_HOSTS.append("testserver")

# ✔ CSRF Origins (MUST be full URLs)
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "").split(",")
    if origin.strip()
]

# ✔ Needed for Heroku reverse proxy
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Clickjacking protection
X_FRAME_OPTIONS = "DENY"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

# ─────────────────────────────────────────────
# APPLICATIONS
# ─────────────────────────────────────────────

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "widget_tweaks",

    # Local apps
    "hospital",
    "payments",  # Stripe / payments app
]

# ─────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # static files on Heroku
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "hospitalmanagement.urls"
WSGI_APPLICATION = "hospitalmanagement.wsgi.application"

# ─────────────────────────────────────────────
# TEMPLATES
# ─────────────────────────────────────────────

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ─────────────────────────────────────────────
# DATABASE — SQLite locally, PostgreSQL on Heroku
# ─────────────────────────────────────────────

# If Heroku has set DATABASE_URL (when Postgres add-on is attached),
# use that. Otherwise fall back to local SQLite.
if "DATABASE_URL" in os.environ:
    DATABASES = {
        "default": dj_database_url.config(
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─────────────────────────────────────────────
# PASSWORD VALIDATION
# ─────────────────────────────────────────────

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────────────────────
# INTERNATIONALIZATION
# ─────────────────────────────────────────────

LANGUAGE_CODE = "en-gb"
TIME_ZONE = "Europe/London"
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────
# STATIC & MEDIA FILES
# ─────────────────────────────────────────────

STATIC_URL = "/static/"

# Where STATICFILES_DIRS exists in development
STATICFILES_DIRS = [STATIC_DIR] if STATIC_DIR.exists() else []

# Where static files are collected for production (Heroku)
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = MEDIA_DIR

# Django 4.2+ storage settings
STORAGES = {
    # Default storage for uploaded files (profile pictures, etc.)
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {
            "location": MEDIA_ROOT,
        },
    },
    # Storage for static files (served via WhiteNoise on Heroku)
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# ─────────────────────────────────────────────
# AUTH REDIRECTS
# ─────────────────────────────────────────────

LOGIN_URL = "/adminlogin/"
LOGIN_REDIRECT_URL = "/afterlogin/"
LOGOUT_REDIRECT_URL = "/"

# ─────────────────────────────────────────────
# EMAIL SETTINGS (Used for notifications)
# ─────────────────────────────────────────────

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True").lower() == "true"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv(
    "DEFAULT_FROM_EMAIL",
    EMAIL_HOST_USER or "no-reply@example.com",
)
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", DEFAULT_FROM_EMAIL)
ADMIN_INVOICE_EMAIL = os.getenv("ADMIN_INVOICE_EMAIL", ADMIN_EMAIL)
EMAIL_RECEIVING_USER = [
    email for email in os.getenv("EMAIL_RECEIVING_USER", "").split(",") if email
]

# ─────────────────────────────────────────────
# STRIPE SETTINGS
# ─────────────────────────────────────────────

# Read from environment; default to empty strings so code doesn't crash
STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY", "")
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
STRIPE_CURRENCY = "gbp"

# Configure Stripe SDK only if we actually have a key
if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

# ─────────────────────────────────────────────
# DEFAULT FIELD TYPE
# ─────────────────────────────────────────────

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?
# LOGGING (Heroku-friendly console logs)
# ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?ƒ"?
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(name)s %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",
            "propagate": False,
        },
        "hospital": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
