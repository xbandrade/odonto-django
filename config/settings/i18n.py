# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

from django.utils.translation import gettext_lazy as _

from . import BASE_DIR

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LANGUAGES = [
    ('en', _('English')),
    ('pt-br', _('Portuguese (Brazil)')),
]
