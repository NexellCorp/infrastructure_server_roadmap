# Copyright (C) 2013 Linaro
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

from django.conf.urls.defaults import (
    patterns,
    url
)

from roadmap.views import (
    roadmap,
    component,
    status,
    search,
    update_card,
    index,
    roadmap_index,
)

urlpatterns = patterns(
    '',
    url(r'^$', index, name="index"),
    url(r'^roadmap/$', roadmap_index),
    url(r'^roadmap/(?P<roadmap_id>\d+)$', roadmap),
    url(r'^component/(?P<roadmap_id>\d+)$', component),
    url(r'^status/(?P<status_id>\d+)$', status),
    url(r'^search$', search),
    url(r'^component/(?P<roadmap_id>\d+)/roadmap$', roadmap),
    url(r'^webhook$', update_card),
)
