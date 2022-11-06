from decouple import config
import os


def set_settings_env():
    DJANGO_SETTINGS_ENV = config("DJANGO_SETTINGS_ENV")

    if DJANGO_SETTINGS_ENV == 'production':
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'core.settings.production')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                              'core.settings.development')
