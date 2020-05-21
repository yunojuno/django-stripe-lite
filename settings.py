"""
Library development settings file.

This settings file is only required so that the project
has a way to using django-admin.py/manage.py to create
migrations. It provides a base set of settings such that
Django can run the migration framework. It should not be
used/imported in day-to-day usage of the library.
"""
from os import getenv

DEBUG = True

SECRET_KEY = "TOP_SECRET"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": getenv("TEST_DB_NAME", "postgres"),
        "USER": getenv("TEST_DB_USER", "postgres"),
        "PASSWORD": getenv("TEST_DB_PASSWORD", "postgres"),
        "HOST": getenv("TEST_DB_HOST", "localhost"),
        "PORT": getenv("TEST_DB_PORT", "5432"),
    }
}

INSTALLED_APPS = (
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_stripe",
)

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": {
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            }
        },
    }
]

ROOT_URLCONF = "django_stripe.urls"

STATIC_ROOT = "static"

STATIC_URL = "/static/"

APPEND_SLASH = True
