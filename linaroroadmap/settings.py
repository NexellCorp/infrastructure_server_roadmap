# Django settings for linaroroadmap project.

DEBUG = True

ADMINS = (
    ('linaro-infrastructure', 'linaro-infrastructure-errors@linaro.org')
)

AUTH_CROWD_ALWAYS_UPDATE_USER = True
AUTH_CROWD_ALWAYS_UPDATE_GROUPS = True
AUTH_CROWD_CREATE_GROUPS = False
AUTH_CROWD_GROUP_MAP = {}
AUTH_CROWD_STAFF_GROUP = 'staff'
AUTH_CROWD_SUPERUSER_GROUP = 'superuser'
AUTH_CROWD_APPLICATION_USER = ''
AUTH_CROWD_APPLICATION_PASSWORD = ''
AUTH_CROWD_SERVER_REST_URI = ''
AUTH_CROWD_SERVER_TRUSTED_ROOT_CERTS_FILE = None

TRUSTED_ADDRESS = []

# The URL of the Jira server to connect to.
JIRA_SERVER = None
# The user name to use to connect to JIRA_SERVER.
JIRA_USERNAME = None
# The password for JIRA_SERVER.
JIRA_PASSWORD = None

JIRA_PROJECT = ''
JIRA_STATUSES = []
# name of the resolutions that remove the closed card from the roadmap
JIRA_INVALID_RESOLUTIONS = []
# Custom field that defines relation between blueprint and engineering card
# in greenhopper
SFID = None

AUTHENTICATION_BACKENDS = (
    #'django.contrib.auth.backends.ModelBackend',
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/linaroroadmap.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

#LANGUAGES = (
#        ('en-us', u'English'),
#)

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

LOGIN_REDIRECT_URL = '/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

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
    'django.middleware.transaction.TransactionMiddleware',
    # 'reversion.middleware.RevisionMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'linaroroadmap.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'linaroroadmap.wsgi.application'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

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
    'reversion',
    'roadmap',
    'south',
    'crowdrest',
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
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)-8s %(message)s',
            'encoding': 'utf8',
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'roadmap_helpers': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/roadmap/roadmap.helpers.log',
            'backupCount': 5,
            'when': 'midnight',
            'formatter': 'simple',
            'encoding': 'utf8',
            'delay': True,
        },
        'roadmap_app': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': '/var/log/roadmap/roadmap.app.log',
            'backupCount': 5,
            'when': 'midnight',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'roadmap.helpers': {
            'level': 'INFO',
            'handlers': ['roadmap_helpers'],
            'propagate': False,
        },
        'roadmap': {
            'level': 'DEBUG',
            'handlers': ['roadmap_app'],
            'propagate': False,
        }
    }
}

UPSTREAM_DEVELOPMENT = "Upstream Development"

try:
    from local_settings import *
except ImportError:
    import random
    import string

    # Create local_settings with random SECRET_KEY.
    char_selection = string.ascii_letters + string.digits
    char_selection_with_punctuation = char_selection + '!@#$%^&*(-_=+)'

    # SECRET_KEY contains anything but whitespace
    secret_key = ''.join(random.sample(char_selection_with_punctuation, 50))
    local_settings_content = "SECRET_KEY = '{0}'\n".format(secret_key)

    with open(os.path.join(PROJECT_ROOT, "local_settings.py"), "w") as f:
        f.write(local_settings_content)

    from local_settings import *

TEMPLATE_DEBUG = DEBUG
