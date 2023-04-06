from django.conf import settings

from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE

if settings.DEBUG and settings.LOCAL_RUN:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True,
    }

INTERNAL_IPS = [
    'localhost', '127.0.0.1',
]
