from pathlib import Path
import os

from bde.env import EnvConfig

env = EnvConfig()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = env.SECRET_KEY
DEBUG = env.DEBUG
ALLOWED_HOSTS = env.ALLOWED_HOSTS

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SESSION_COOKIE_SECURE = env.SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = env.CSRF_COOKIE_SECURE

if env.CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS = env.CSRF_TRUSTED_ORIGINS

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "whitenoise.runserver_nostatic",
    "mozilla_django_oidc",
    "members",
    "showcase",
]

MYPY_PLUGINS = ["mypy_django_plugin.main"]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    # "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "auth.auth_backends.CustomOIDCBackend",
]

LOGIN_URL = f"/{env.ADMIN_URL}login/"
LOGIN_REDIRECT_URL = f"/{env.ADMIN_URL}"
LOGOUT_REDIRECT_URL = "/"

OIDC_OP_AUTHORIZATION_ENDPOINT = env.OIDC_OP_AUTHORIZATION_ENDPOINT
OIDC_OP_TOKEN_ENDPOINT = env.OIDC_OP_TOKEN_ENDPOINT
OIDC_OP_USER_ENDPOINT = env.OIDC_OP_USER_ENDPOINT
OIDC_OP_JWKS_ENDPOINT = env.OIDC_OP_JWKS_ENDPOINT
OIDC_RP_CLIENT_ID = env.OIDC_RP_CLIENT_ID
OIDC_RP_CLIENT_SECRET = env.OIDC_RP_CLIENT_SECRET
OIDC_RP_SIGN_ALGO = env.OIDC_RP_SIGN_ALGO
OIDC_RP_SCOPES = env.OIDC_RP_SCOPES

ROOT_URLCONF = "bde.urls"

SESSION_COOKIE_SECURE = env.SESSION_COOKIE_SECURE
CSRF_COOKIE_SECURE = env.CSRF_COOKIE_SECURE

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "templates"),
            os.path.join(BASE_DIR, "bde/templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "bde.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env.DB_NAME,
        "USER": env.DB_USER,
        "PASSWORD": env.DB_PASSWORD,
        "HOST": env.DB_HOST,
        "PORT": env.DB_PORT,
        "OPTIONS": {"init_command": "SET sql_mode='STRICT_TRANS_TABLES'"},
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
# STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/uploads/"
MEDIA_ROOT = BASE_DIR / "uploads"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
