USE_I18N = False
SECRET_KEY = "test_secret_key"

INSTALLED_APPS = ["django_wait_for_databases"]

LOGGING = {
    "version": 1,  # the dictConfig format version
    "disable_existing_loggers": False,  # retain the default loggers
    "handlers": {
        "console": {"class": "logging.StreamHandler", "level": "DEBUG"},
    },
    "loggers": {
        "django": {"level": "DEBUG", "handlers": ["console"]},
        "django_wait_for_databases": {"level": "DEBUG", "handlers": ["console"]},
    },
}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/db.sqlite3",
    },
    "postgres": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "postgres",
        "PORT": "5432",
        "NAME": "test",
        "USER": "test",
        "PASSWORD": "test",
    },
}
