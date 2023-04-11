import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'INSECURE')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', '1') == '1'

LOCAL_RUN = os.environ.get('LOCAL_RUN', '1') == '1'

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS', 'localhost'
).strip().split(',')

CSRF_TRUSTED_ORIGINS = os.environ.get(
    'CSRF_TRUSTED_ORIGINS', 'https://localhost'
).strip().split(',')

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.app'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
