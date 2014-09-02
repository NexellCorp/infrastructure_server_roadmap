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

import logging

from django.core.management.base import (
    BaseCommand,
    CommandError
)
from django.conf import settings
from jira.client import JIRA
from optparse import make_option
from roadmap.helpers import (
    create_or_update,
    JIRA_VERIFY,
    JIRA_DEPENDSON,
    JIRA_IMPLEMENTS,
    JIRA_KEY,
    SINGLE_UPDATE,
    DEBUG
)

log = logging.getLogger('roadmap.helpers')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            '--key',
            dest=JIRA_KEY,
            action='store',
            type='string',
            help="Jira issue key. Only this issue is synced"
        ),
        make_option(
            '--no-implements',
            dest=JIRA_IMPLEMENTS,
            action='store_false',
            default=True,
            help=("If set the 'implements' relations are not retrieved. "
                  "Default: false")
        ),
        make_option(
            '--depends',
            dest=JIRA_DEPENDSON,
            action='store_true',
            default=False,
            help=("If set the 'depends' relations are not retrieved. Default: "
                  "false. Be careful when not using --no-implements might "
                  "run into infinite loop.")
        ),
        make_option(
            '--no-verify',
            dest=JIRA_VERIFY,
            action='store_false',
            default=True,
            help=("If set allows to connect to Jira server secured with "
                  "self-signed certificate")
        ),
        make_option(
            '--debug',
            dest=DEBUG,
            action='store_true',
            default=False,
            help='Enables debug logging. Default: false.'
        ),
    )
    help = 'Imports current snapshot from Jira server'

    def handle(self, *args, **options):
        if options[DEBUG]:
            log.setLevel(logging.DEBUG)

        if settings.JIRA_SERVER is None:
            raise CommandError("Missing Jira server parameter.")
        if settings.JIRA_USERNAME is None:
            raise CommandError("Missing Jira username parameter.")
        if settings.JIRA_PASSWORD is None:
            raise CommandError("Missing Jira password parameter.")

        jira_options = {
            'server': settings.JIRA_SERVER,
            'verify': options[JIRA_VERIFY]}
        jira = JIRA(
            options=jira_options,
            basic_auth=(settings.JIRA_USERNAME, settings.JIRA_PASSWORD)
        )

        start = 0

        if options[JIRA_KEY] is None:
            issues = jira.search_issues(
                'project="{0}"'.format(settings.JIRA_PROJECT),
                startAt=start,
                expand="changelog")
        else:
            issues = jira.search_issues(
                'key="{0}"'.format(options[JIRA_KEY]),
                startAt=start,
                expand="changelog")

        options.update({SINGLE_UPDATE: False})
        log.info("Total issues: {0}".format(issues.total))

        while len(issues) > 0:
            for index, issue in enumerate(issues, start=1):
                log.info("Processing issue {0}/{1} ({2}/{3}) {4}".format(
                    index+start, issues.total, index, len(issues), issue.key))

                create_or_update(issue, options, jira)

            start += len(issues)

            log.info("Searching issues starting at {0}".format(start))
            if options[JIRA_KEY] is None:
                issues = jira.search_issues(
                    'project="{0}"'.format(settings.JIRA_PROJECT),
                    startAt=start,
                    expand="changelog")
            else:
                issues = jira.search_issues(
                    'key="{0}"'.format(options[JIRA_KEY]),
                    startAt=start,
                    expand="changelog")
