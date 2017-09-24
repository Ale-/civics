"""
Django settings for civics project
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.abspath( os.path.dirname(__file__) )
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(ENV_PATH, '..', 'static')
PROJECT_STATIC_FOLDER = 'civics'
STATICFILES_DIRS = [
    ( PROJECT_STATIC_FOLDER, STATIC_ROOT + '/' + PROJECT_STATIC_FOLDER + '/' ),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(ENV_PATH, '..', 'media')
MAINTENANCE_IGNORE_URLS = (
    r'^/admin/.*',
    r'^/login$',
)
LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/mi-perfil'
LOGOUT_URL = '/logout'
LOGOUT_REDIRECT_URL = '/gracias'

ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_OPEN = True

# Name of site in the document title
DOCUMENT_TITLE = 'Civics'
DOCUMENT_DESCRIPTION = _('Aquí podrás encontrar iniciativas ciudadanas existentes en tu ciudad, etc.')

# Sites conf
SITE_ID = 1

#
# Application definition
#

CONTRIB_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maintenancemode',
    'leaflet',
    'djgeojson',
    'imagekit',
    'django_countries',
]

PROJECT_APPS = [
    'apps.models',
    'apps.utils',
    'apps.users',
    'apps.api',
]

INSTALLED_APPS = CONTRIB_APPS + PROJECT_APPS

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'civics.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.utils.context_processors.site_info_processor',
                'apps.utils.context_processors.debug_processor',
                'apps.users.context_processors.current_user_hello',
            ],
        },
    },
]

WSGI_APPLICATION = 'civics.wsgi.application'

#
# Password validation
#
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

#
# Internationalization
#
LANGUAGE_CODE = 'es'
LANGUAGES = (
    ('es', _('Español')),
    ('pt', _('Portugués')),
)
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
DECIMAL_SEPARATOR = '.'

#
# Leaflet
#

LEAFLET_CONFIG = {
    'DEFAULT_CENTER': (-15, -26),
    'DEFAULT_ZOOM'  : 2,
    'MIN_ZOOM'      : 2,
    'MAX_ZOOM'      : 18,
}

#
# Import private settings
#
from .private_settings import *
