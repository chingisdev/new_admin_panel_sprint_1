import os

from config.settings.components.common import INSTALLED_APPS, \
    MIDDLEWARE

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
DEBUG = True

INSTALLED_APPS += [
    'debug_toolbar'
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]
