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

import logging

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
from roadmap.helpers import (
    collect_burndown,
    collect_component_burndown,
    DEBUG,
)
from roadmap.models import Project, CardType

BURNDOWN_PROJECT = 'project'
BURNDOWN_CARDTYPE = 'cardtype'

log = logging.getLogger("roadmap.helpers")


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--project',
            dest=BURNDOWN_PROJECT,
            action='store',
            type='string',
            help='Project name to create the burndown for',
            default=settings.JIRA_PROJECT
        ),
        make_option(
            '--card-type',
            dest=BURNDOWN_CARDTYPE,
            action='store',
            type='string',
            help='Jira issue type to aggregate the values for',
            default='Blueprint'
        ),
        make_option(
            '--debug',
            dest=DEBUG,
            action='store_true',
            default=False,
            help='Enables debug logging. Default: false.'
        ),
    )
    help = 'Collects the aggregate data to create the burndown bars'

    def handle(self, *args, **options):
        if options[DEBUG]:
            log.setLevel(logging.DEBUG)

        project = Project.objects.get(name=options[BURNDOWN_PROJECT])
        card_type = CardType.objects.get(name=options[BURNDOWN_CARDTYPE])
        collect_burndown(project, card_type)
        collect_component_burndown(project)
