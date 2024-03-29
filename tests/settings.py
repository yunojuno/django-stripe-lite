#############################################
# Relevant django-stripe-lite test settings #
#############################################

STRIPE_WEBHOOK_SECRET = "whsec_0DoBceBjS0jjm7aQj459FXiFSluJEBxt"
ROOT_URLCONF = "tests.urls"

############################
# Required Django Settings #
############################

DEBUG = True

SECRET_KEY = "TOP_SECRET"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test.db",
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
    "tests",
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
                "django.template.context_processors.request",
            }
        },
    }
]


STATIC_ROOT = "static"

STATIC_URL = "/static/"

APPEND_SLASH = True

assert DEBUG, "This application should be used for local testing only"
