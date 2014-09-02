#!/bin/bash
# Copyright (C) 2013, 2014 Linaro
#
# This file is part of roadmap.
#
# roadmap is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# roadmap is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with roadmap.  If not, see <http://www.gnu.org/licenses/>.

export WORKON_HOME={{install_base }}/virtualenv
source /usr/local/bin/virtualenvwrapper.sh

workon {{ install_dir }}

cd /srv/{{ install_dir }}

{% if role == 'staging' %}
./manage.py roadmap_import --debug
./manage.py burndown_snapshot --debug
{% else %}
./manage.py roadmap_import
./manage.py burndown_snapshot
{% endif %}