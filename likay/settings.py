# Django settings for likay project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'likay.db',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '2ac!l8+vhah_cuk=8bo=7vdqfdg5dj!f8-^u!vq*u@8jk77v7s'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


#########
# PATHS #
#########

import os

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

PROJECT_DIRNAME = PROJECT_ROOT.split(os.sep)[-1]

CACHE_MIDDLEWARE_KEY_PREFIX = PROJECT_DIRNAME

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(PROJECT_ROOT, STATIC_URL.strip("/"))

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(PROJECT_ROOT, MEDIA_URL.strip("/"))

ROOT_URLCONF = "%s.urls" % PROJECT_DIRNAME

TEMPLATE_DIRS = (os.path.join(PROJECT_ROOT, "templates"),)

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'likay.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',

    # third party apps
    'south',
    
    # local apps
    'likay',
    'accounts',
    'core',
    'sms',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

############
# Facebook #
############

FACEBOOK_APPLICATION_ID = 181259711925270
FACEBOOK_APPLICATION_SECRET_KEY = '214e4cb484c28c35f18a70a3d735999b'
FACEBOOK_APPLICATION_NAMESPACE = 'likayph'

FACEBOOK_PAGE_ID = '248804028611316'
POST_ACCESS_TOKEN = 'CAACk2tC9zBYBAMdeGodZAJ00JNfPZBZAOzxUZBtlBJt2COY05tZBZAIoL2AkT5npsQHRtRvlzquqT7TpeQDZANrWqped3PnQJhdIuZC0jqsD23FTUIImgE2qLELcHxkVXE2ZBGX1U9Xq0p4ufJLi3s9iKjYZAFPMdxdhv8DJ2q6IMLBN4swKVjZBVs2NOS16lCs3HAZD'

######################
# YOUPHORIC SETTINGS #
######################
YOUPHORIC_TEST_MODE = True

# The YouPhoric account ID which requires credits to do outbound messages
ACCOUNT_ID = 'c5f7bd18254fb2050e47b9749a485b12'

# The user will send messages to this number (exclusive for SMART subscribers)
ACCESS_CODE = '68002' 

# Add 'accountId', 'msisdn', and 'text' as GET parameters in this URL to send an outbound message
OUTBOUND_URL = 'http://121.58.235.158/angelhack/smsout.php'

###########################
# TWITTER KEYS AND TOKENS #
###########################
TWITTER_CONSUMER_KEY = '9cqozV0HpETI89dIEvyLTA'
TWITTER_CONSUMER_SECRET = 'o3ov3PRSUhWvrN6N7cHbG1o3VSivsfv3bH6BEW6nnM'
TWITTER_ACCESS_TOKEN ='2210852508-wneJzBPPzv7LOjEnkIZzwBUZLq571Yolug5wl5q'
TWITTER_ACCESS_TOKEN_SECRET = '7yeB7GyZ7aTGP6OLMeTSRzqE3Vcu5kIOiIxi1jZ3nJmZf'

try:
    from local_settings import *
except ImportError:
    pass
