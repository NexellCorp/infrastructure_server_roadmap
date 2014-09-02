import os
import sys
import site

# Add the site-packages of the chosen virtualenv to work with
site.addsitedir('{{ install_base }}/virtualenv/{{ install_dir }}/'
                'local/lib/python2.7/site-packages')

# Add the app's directory to the PYTHONPATH
sys.path.append('{{ install_base }}/{{ install_dir }}/')
sys.path.append('{{ install_base }}/{{ install_dir }}/linaroroadmap/')

os.environ['DJANGO_SETTINGS_MODULE'] = 'linaroroadmap.settings'

# Activate your virtual env
activate_env = os.path.expanduser(
    "{{ install_base }}/virtualenv/{{ install_dir }}/bin/activate_this.py")
execfile(activate_env, dict(__file__=activate_env))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
