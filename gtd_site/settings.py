import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "local-dev-only-not-secret"
DEBUG = True
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "rest_framework",
    "gtd_core",
    "gtd_api",
    "bear_reader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "gtd_site.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "gtd_site.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
FRONTEND_DIR = BASE_DIR / "frontend" / "dist"
STATICFILES_DIRS = [FRONTEND_DIR] if FRONTEND_DIR.exists() else []

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
    "DEFAULT_PARSER_CLASSES": ["rest_framework.parsers.JSONParser"],
    "UNAUTHENTICATED_USER": None,
}

GTD_DATA_ROOT = Path(os.environ.get("GTD_DATA_ROOT", BASE_DIR / "data"))

BEAR_DB_PATH = Path(
    os.environ.get(
        "BEAR_DB_PATH",
        "~/Library/Group Containers/9K33E3U3T4.net.shinyfrog.bear/Application Data/database.sqlite",
    )
).expanduser()

# AI capture shells out to the `claude` CLI which uses the user's Max plan
# credentials — no ANTHROPIC_API_KEY needed. ANTHROPIC_MODEL picks which model.
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-6")

# Working dir for `🤖 agent` Terminal launches. Defaults to the canary monorepo
# so the spawned `claude` session has the right code context out of the box.
GTD_AGENT_CWD = Path(os.environ.get("GTD_AGENT_CWD", "~/projects/canary")).expanduser()

LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "[%(asctime)s] %(levelname)s %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "access": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "default"},
        "app_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOGS_DIR / "gtd.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "default",
            "delay": True,
        },
        "gunicorn_access_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOGS_DIR / "access.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "access",
            "delay": True,
        },
        "gunicorn_error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": str(LOGS_DIR / "error.log"),
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "default",
            "delay": True,
        },
    },
    "root": {"handlers": ["console", "app_file"], "level": "INFO"},
    "loggers": {
        "gunicorn.access": {
            "handlers": ["gunicorn_access_file"],
            "level": "INFO",
            "propagate": False,
        },
        "gunicorn.error": {
            "handlers": ["gunicorn_error_file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
