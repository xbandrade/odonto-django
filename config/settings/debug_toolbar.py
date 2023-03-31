from django.conf import settings

from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE

if settings.DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE
    INTERNAL_IPS = [
        'localhost',
    ]
