import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('/srv/virtualenv/roadmap/local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('/srv/roadmap.linaro.org/')
sys.path.append('/srv/roadmap.linaro.org/linaroroadmap/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'linaroroadmap.settings'

# Activate your virtual env
activate_env = os.path.expanduser(
    "/srv/virtualenv/roadmap/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
