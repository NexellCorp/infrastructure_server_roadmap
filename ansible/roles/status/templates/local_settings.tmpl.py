import random
import string

AUTH_CROWD_ALWAYS_UPDATE_USER = False
AUTH_CROWD_ALWAYS_UPDATE_GROUPS = False
AUTH_CROWD_APPLICATION_USER = '{{ crowd_app_name }}'
AUTH_CROWD_APPLICATION_PASSWORD = '{{ crowd_app_password }}'
AUTH_CROWD_SERVER_REST_URI = '{{ crowd_url }}'

TRUSTED_ADDRESS = ['10.101.63.171', '10.137.64.8', '82.22.217.167',
                   '10.191.101.11', '10.165.3.8', '10.215.86.3']

JIRA_SERVER = '{{ jira_server }}'
JIRA_USERNAME = '{{ jira_username }}'
JIRA_PASSWORD = '{{ jira_password }}'

JIRA_PROJECT = 'Linaro Roadmap'
JIRA_STATUSES = ['Closed', 'Resolved', 'In Progress', 'Open', 'Reopened']
JIRA_INVALID_RESOLUTIONS = ['Incomplete', 'Deferred', 'Cancelled', 'Duplicate']
SFID = {{ jira_sfid }}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '{{ install_base }}/{{ install_dir }}/linaroroadmap.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

AUTHENTICATION_BACKENDS = (
    'crowdrest.backend.CrowdRestBackend',
)

char_selection = string.ascii_letters + string.digits
char_selection += '!@#$%^&*(-_=+)'

SECRET_KEY = '{0}'.format(''.join(random.sample(char_selection, 50)))

STATIC_ROOT = '/var/www/{{ install_dir }}/static/'
{% if role == 'staging' %}
DEBUG = True
{% else %}
DEBUG = False
{% endif %}
