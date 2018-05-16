import os
import sys
import dj_database_url
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS = [
    'blog',
    'cefet',
    'members',
    'staff',
    'events',
    'django_nose',
    'django_summernote',
    'sorl.thumbnail',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dbbackup', 
    'storages',# django-dbbackup
    'django_cron',
    ]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'site_pet.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates').replace('\\', '/'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
            ],
        },
    },
]

TEMPLATES[0]['OPTIONS']['context_processors'].append('cefet.context_processors.pets_processor')

WSGI_APPLICATION = 'site_pet.wsgi.application'

###########################################################
#mysql                                                    #
###########################################################
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'site_pet', #DB_NAME
        'USER': 'compet', #DB_USER
        'PASSWORD': '.compet2015', #DB_PASSWORD
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

###########################################################
#sqlite3                                                  #
###########################################################
#DATABASES = {
#    'default':{
#        'ENGINE':'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR,'tmp.db.sqlite3'),
#    } #dj_database_url.config()
#}

#if 'test' in sys.argv or 'test_coverage' in sys.argv:
#    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

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

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles/')
MEDIA_URL = '/media/'

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

LOGIN_URL = '/staff/login'

SUMMERNOTE_CONFIG = {
    'lang': 'pt-BR',
    'width': '100%',
}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'


EMAIL_HOST = 'smtp.sendgrid.net' # adicionar as duas variaveis abaixo no arquivo (bin/activate) 
EMAIL_HOST_USER = os.getenv('EMAIL_ADDRESS') # (Login no sendgrid) -> export EMAIL_ADDRESS = 'exemplo'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD') # (Senha do sendgrid) -> export EMAIL_PASSWORD = 'exemplo'
EMAIL_PORT = 587
iEMAIL_USE_TLS = True
CRON_CLASSES = [
    "site_pet.django-cron.Backup",
    # ...
]
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': 'database/'}

GPG_ALWAYS_TRUST = getattr(settings, 'DBBACKUP_GPG_ALWAYS_TRUST', False)
GPG_RECIPIENT = GPG_ALWAYS_TRUST = getattr(settings, 'DBBACKUP_GPG_RECIPIENT', None)
