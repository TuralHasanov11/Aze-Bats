from pathlib import Path
from decouple import config
import dj_database_url
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
import os
from django.utils.log import DEFAULT_LOGGING


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY")

DEBUG = config("DJANGO_DEBUG", cast=bool)

ALLOWED_HOSTS = str(config("ALLOWED_HOSTS", default="")).split(",") or []

if DEBUG:
    ALLOWED_HOSTS += ["127.0.0.1", "localhost"]


CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_TRUSTED_ORIGINS = str(config("ALLOWED_ORIGINS", "")).split(",") or []
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    
    "rosetta",
    "log_viewer",
    "csp",
    "axes",
    'django_cleanup.apps.CleanupConfig',
    'tinymce',
    
    "apps.home",
    "apps.species",
    "apps.activities",
    "apps.articles",
    "apps.shared",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.gzip.GZipMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "csp.middleware.CSPMiddleware",
    "axes.middleware.AxesMiddleware",
    "maintenance_mode.middleware.MaintenanceModeMiddleware"
]

ROOT_URLCONF = "web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "apps/shared/templates/shared"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "csp.context_processors.nonce",
                "apps.home.context_processors.home_context",
                "apps.home.context_processors.base_menu",
                "apps.home.context_processors.search_form",
                "apps.species.context_processors.families",
                "apps.species.context_processors.genus_count",
                "apps.species.context_processors.bat_count",
            ],
        },
    },
]

WSGI_APPLICATION = "web.wsgi.application"
ASGI_APPLICATION = "web.asgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

if config("POSTGRES_DB_READY", cast=bool):
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB"),
        "USER": config("POSTGRES_USER"),
        "PASSWORD": config("POSTGRES_PASSWORD"),
        "HOST": config("POSTGRES_HOST"),
        "PORT": config("POSTGRES_PORT"),
    }

DATABASE_URL = str(config("DATABASE_URL", default=""))
if DATABASE_URL:
    DATABASES["default"].update(
        dj_database_url.config(
            default=DATABASE_URL, conn_max_age=1800, conn_health_checks=True
        )
    )


AUTHENTICATION_BACKENDS = [
    "axes.backends.AxesStandaloneBackend",
    "django.contrib.auth.backends.ModelBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 12,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/admin/"


TIME_ZONE = "Asia/Baku"

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGE_CODE = "az"

LANGUAGES = (
    ("az", _("Azerbaijani")),
    ("en", _("English")),
)

LOCALE_PATHS = (BASE_DIR / "locale/",)


STATIC_URL = "static/"
STATICFILES_BASE_DIR = BASE_DIR / "static"
STATICFILES_BASE_DIR.mkdir(exist_ok=True, parents=True)
STATICFILES_DIRS = [
    STATICFILES_BASE_DIR
]

MEDIA_URL = "/media/"
if not DEBUG:
    MEDIA_ROOT = "/home/azeribat/public_html/media/"
    STATIC_ROOT = "/home/azeribat/public_html/static/"
else:
    MEDIA_ROOT = BASE_DIR / "media"
    STATIC_ROOT = BASE_DIR / "static-cdn"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


SITE_ID = 1


if DEBUG:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", cast=str, default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=str, default="587")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", cast=str, default=None)
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", cast=str, default=None)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool, default=True)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", cast=bool, default=False)
EMAIL_USE_LOCALTIME = config("EMAIL_USE_LOCALTIME", cast=bool, default=True)


MAINTENANCE_MODE = config("MAINTENANCE_MODE", cast=bool, default=False)
MAINTENANCE_BYPASS_QUERY = config("MAINTENANCE_BYPASS_QUERY", default="bypass")
MAINTENANCE_MODE_IGNORE_ADMIN_SITE = True
MAINTENANCE_MODE_IGNORE_STAFF = True
MAINTENANCE_MODE_IGNORE_SUPERUSER = True

CSP_DEFAULT_SRC = ("'self'", )
CSP_CONNECT_SRC = ("'self'", )
CSP_STYLE_SRC = ("'self'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net", "fonts.googleapis.com")
CSP_SCRIPT_SRC = ("'self'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net", "'unsafe-inline'")
CSP_IMG_SRC = ("'self'", )
CSP_FONT_SRC = ("'self'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net", "https://fonts.gstatic.com")
CSP_INCLUDE_NONCE_IN = ['script-src', "style-src"]

MESSAGE_TAGS = {
    messages.constants.DEBUG: "alert-secondary",
    messages.constants.INFO: "alert-info",
    messages.constants.SUCCESS: "alert-success",
    messages.constants.WARNING: "alert-warning",
    messages.constants.ERROR: "alert-danger",
}


LOG_DIR = BASE_DIR / "logs"
LOG_FILE = "/info.log"
LOG_PATH = f"{LOG_DIR}/{LOG_FILE}"
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

if not os.path.exists(LOG_PATH):
    f = open(LOG_PATH, "w").close()
else:
    f = open(LOG_PATH, "a").close()

LOGGING_CONFIG = None
LOGLEVEL = os.environ.get("LOGLEVEL", "info").upper()
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s at %(name)-2s in %(module)s with level %(levelname)-2s : %(message)s",
        },
        "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
    },
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
    },
    "handlers": {
        "console": {
            "level": LOGLEVEL,
            "filters": ["require_debug_true"],
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "level": LOGLEVEL,
            "formatter": "default",
            "class": "logging.FileHandler",
            "filename": LOG_PATH,
            "encoding": "utf8",
        },
        "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
    },
    "loggers": {
        "": {
            "level": LOGLEVEL,
            "handlers": ["file", "console"],
        },
        "django": {
            "handlers": ["file", "console"],
            "propagate": False,
        },
        "django.request": {
            "handlers": ["file", "console"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        "apps.home": {
            "handlers": DEBUG and ["file", "console"] or ["file"],
            "propagate": False,
            "level": LOGLEVEL,
        },
        "apps.activities": {
            "handlers": DEBUG and ["file", "console"] or ["file"],
            "propagate": False,
            "level": LOGLEVEL,
        },
        "apps.articles": {
            "handlers": DEBUG and ["file", "console"] or ["file"],
            "propagate": False,
            "level": LOGLEVEL,
        },
        "apps.species": {
            "handlers": DEBUG and ["file", "console"] or ["file"],
            "propagate": False,
            "level": LOGLEVEL,
        },
        "apps.shared": {
            "handlers": DEBUG and ["file", "console"] or ["file"],
            "propagate": False,
            "level": LOGLEVEL,
        },
    },
}

LOG_VIEWER_FILES = ["main.log"]
LOG_VIEWER_FILES_PATTERN = "*.log*"
LOG_VIEWER_FILES_DIR = "logs/"
LOG_VIEWER_PAGE_LENGTH = 25
LOG_VIEWER_MAX_READ_LINES = 1000
LOG_VIEWER_FILE_LIST_MAX_ITEMS_PER_PAGE = 25
LOG_VIEWER_PATTERNS = ["[INFO]", "[DEBUG]", "[WARNING]", "[ERROR]", "[CRITICAL]"]
LOG_VIEWER_EXCLUDE_TEXT_PATTERN = None


AXES_ENABLED = True
AXES_COOLOFF_TIME = config("AXES_COOLOFF_TIME", default=0.25, cast=float)
AXES_FAILURE_LIMIT = config("AXES_FAILURE_LIMIT", default=10, cast=int)
AXES_RESET_ON_SUCCESS = True
AXES_USERNAME_FORM_FIELD = "username"
AXES_LOCKOUT_PARAMETERS = [["username", "user_agent"]]


X_FRAME_OPTIONS = "ALLOW-FROM https://www.youtube.com/"


APP_NAME = os.environ.get("APP_NAME", "AzeriBats")


TINYMCE_DEFAULT_CONFIG = {
    "height": 1000,
    "menubar": "file edit view insert format tools table help",
    "plugins": "advlist autolink lists link image charmap preview anchor searchreplace visualblocks code "
    "fullscreen insertdatetime media table code help wordcount",
    "toolbar": "undo redo | bold italic underline strikethrough | fontselect fontsizeselect formatselect | alignleft "
    "aligncenter alignright alignjustify | outdent indent |  numlist bullist checklist | forecolor "
    "backcolor casechange permanentpen formatpainter removeformat | pagebreak | charmap emoticons | "
    "fullscreen  preview save | insertfile image media pageembed template link anchor codesample | "
    "a11ycheck ltr rtl | showcomments addcomment code",
    "custom_undo_redo_levels": 10,
    "language": "en",
}