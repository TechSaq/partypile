from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

STATIC_URL = "/static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'assets')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
