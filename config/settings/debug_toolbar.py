from .environment import DEBUG, LOCAL_RUN
from .installed_apps import INSTALLED_APPS
from .middlewares import MIDDLEWARE

if DEBUG and LOCAL_RUN:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware', ] + MIDDLEWARE
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: False,
    }

INTERNAL_IPS = [
    'localhost', '127.0.0.1',
]
