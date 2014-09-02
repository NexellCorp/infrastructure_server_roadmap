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

from django.conf import settings
from django.db.models import ManyToManyField
from django.utils import timezone
from datetime import datetime
from operator import attrgetter
from roadmap.models import (
    Burndown,
    BurndownBar,
    BurndownSnapshot,
    Card,
    CardType,
    Component,
    FixVersion,
    Label,
    Milestone,
    Project,
    Resolution,
    SecurityLevel,
    Status,
)

JIRA_SERVER = 'jira_server'
JIRA_USER = 'jira_user'
JIRA_VERIFY = 'jira_verify'
JIRA_DEPENDSON = 'dependson'
JIRA_IMPLEMENTS = 'implements'
JIRA_KEY = 'key'
DEBUG = 'debug'
SINGLE_UPDATE = 'single_update'

log = logging.getLogger('roadmap.helpers')


class Issue(object):

    def __init__(self, d):
        for a, b in d.iteritems():
            if isinstance(b, (list, tuple)):
                setattr(self, a,
                        [Issue(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, Issue(b) if isinstance(b, dict) else b)


def create_or_update(issue, options, jira=None):

    if isinstance(issue, dict):
        issue = Issue(issue)

    log.debug("Creating or updating issue {0}".format(issue.key))

    project = None
    if hasattr(issue.fields, 'project') and issue.fields.project:
        project, created = Project.objects.get_or_create(
            name=issue.fields.project.name, key=issue.fields.project.key)

    card_type = None
    if hasattr(issue.fields, 'issuetype') and issue.fields.issuetype:
        card_type, created = CardType.objects.get_or_create(
            name=issue.fields.issuetype.name)

    resolution = None
    if hasattr(issue.fields, 'resolution') and issue.fields.resolution:
        resolution, created = Resolution.objects.get_or_create(
            name=issue.fields.resolution.name, project=project)

    security = None
    if hasattr(issue.fields, 'security') and issue.fields.security:
        security, created = SecurityLevel.objects.get_or_create(
            name=issue.fields.security.name)

    components = []
    if hasattr(issue.fields, 'components') and issue.fields.components:
        for comp in issue.fields.components:
            cp, created = Component.objects.get_or_create(
                name=comp.name, project=project)
            components.append(cp.pk)
            log.debug("{0}: {1}".format(issue.key, cp.name))
    else:
        log.info("Issue {0} has no component".format(issue.key))

    fixVersion = None
    fixVersions = []
    if hasattr(issue.fields, 'fixVersions') and issue.fields.fixVersions:
        # find the fixVersion in db or create one
        for fixv in issue.fields.fixVersions:
            fix_date = timezone.make_aware(
                datetime(2015, 1, 1),
                timezone.get_default_timezone())
            if hasattr(fixv, "releaseDate"):
                fix_date = timezone.make_aware(
                    datetime.strptime(fixv.releaseDate, "%Y-%m-%d"),
                    timezone.get_default_timezone())
            fv, created = FixVersion.objects.get_or_create(
                name=fixv.name,
                fix_date=fix_date,
                project=project
            )
            fixVersions.append(fv)

        fixVersion = min(fixVersions, key=attrgetter('fix_date'))
        log.debug("Fix version is: {0}".format(fixVersion))

    status = None
    if hasattr(issue.fields, 'status') and issue.fields.status:
        # find status in database or create one
        status, created = Status.objects.get_or_create(
            name=issue.fields.status.name, project=project)
        log.debug("Status is: {0}".format(status))

    cardStart = None
    cardEnd = None
    if fixVersion:
        if fixVersion.name == "ONGOING":
            if (hasattr(issue.fields, 'customfield_10300')
                    and issue.fields.customfield_10300):
                cardStart = issue.fields.customfield_10300
            if hasattr(issue, "changelog"):
                for history in issue.changelog.histories:
                    for item in history.items:
                        if (item.field == "status"
                                and item.toString == "Closed"):
                            cardEnd = datetime.strptime(
                                history.created,
                                "%Y-%m-%dT%H:%M:%S.000+0000").isoformat()
                            if cardStart:
                                break
        else:
            cardStart = fixVersion.fix_date
        log.debug("Start: {0} - End: {1}".format(cardStart, cardEnd))

    upstream_development_name = settings.UPSTREAM_DEVELOPMENT
    if status.name == upstream_development_name:
        if hasattr(issue, "changelog"):
            for history in issue.changelog.histories:
                for item in history.items:
                    if (item.field == "status" and
                            item.toString == upstream_development_name):
                        cardStart = datetime.strptime(
                            history.created,
                            "%Y-%m-%dT%H:%M:%S.000+0000").isoformat()
                    if (item.field == "status" and
                            item.toString == "Closed"):
                        cardEnd = datetime.strptime(
                            history.created,
                            "%Y-%m-%dT%H:%M:%S.000+0000").isoformat()
        if not cardEnd and fixVersion:
            if fixVersion.name != "ONGOING":
                cardEnd = fixVersion.fix_date
        log.debug("Start: {0} - End: {1}".format(cardStart, cardEnd))

    implementedby_list = []
    depends_list = []
    if hasattr(issue.fields, 'issuelinks'):
        for link in issue.fields.issuelinks:
            if link.type.name == "Implements" and options[JIRA_IMPLEMENTS]:
                if hasattr(link, "inwardIssue"):
                    if jira:
                        implementedby_list.append(
                            create_or_update(
                                jira.issue(link.inwardIssue.key,
                                           expand="changelog"),
                                options, jira).pk)
                    elif not options[SINGLE_UPDATE]:
                        implementedby_list.append(
                            create_or_update(
                                link.inwardIssue, options, jira).pk)
                    else:
                        # don't do full update on related cards
                        try:
                            implementedby_list.append(
                                Card.objects.get(key=link.inwardIssue.key))
                        except Exception as ex:
                            log.error("Card not found")
                            log.exception(ex)

            if link.type.name == "Depends" and options[JIRA_DEPENDSON]:
                if hasattr(link, "inwardIssue"):
                    if jira:
                        depends_list.append(
                            create_or_update(
                                jira.issue(
                                    link.inwardIssue.key, expand="changelog"),
                                options, jira).pk)
                    elif not options[SINGLE_UPDATE]:
                        depends_list.append(
                            create_or_update(
                                link.inwardIssue, options, jira).pk)
                    else:
                        # don't do full update on related cards
                        try:
                            depends_list.append(
                                Card.objects.get(key=link.inwardIssue.key))
                        except Exception as ex:
                            log.error("Card not found")
                            log.exception(ex)

    blueprints = []
    if (hasattr(issue.fields, 'issuetype') and
            issue.fields.issuetype.name == "Engineering card"):
        log.debug("Engineering card {0}".format(issue.key))

        bp_search_string = "cf[%s] = %s" % (settings.SFID, issue.key)
        bp_issues = jira.search_issues(bp_search_string)
        start = 0
        while len(bp_issues) > 0:
            for index, blueprint in enumerate(bp_issues, start=1):
                log.debug("Processing Blueprint {0}/{1} ({2}/{3}) {4}".format(
                    index + start, bp_issues.total, index, len(bp_issues),
                    blueprint.key))

                blueprints.append(
                    create_or_update(
                        jira.issue(blueprint.key, expand="changelog"),
                        options, jira).pk)

            start += len(bp_issues)
            bp_issues = jira.search_issues(bp_search_string, startAt=start)
    # compare implemented by and blueprints to eliminate duplicates
    # implementedby_list = set(implementedby_list) | set(blueprints)
    implementedby_list = list(set(implementedby_list).union(set(blueprints)))

    log.debug("Dependencies: {0}".format(depends_list))
    log.debug("Implements: {0}".format(implementedby_list))

    label_list = []
    if hasattr(issue.fields, 'labels'):
        for label in issue.fields.labels:
            lbl_list = Label.objects.filter(name=label)
            if lbl_list:
                label_list.append(lbl_list[0].pk)
            else:
                lbl = Label(name=label)
                lbl.save()
                label_list.append(lbl.pk)

    url = settings.JIRA_SERVER + "/browse/" + issue.key
    summary = issue.fields.summary

    defaults = {
        'url': url,
        'summary': summary,
        'resolution': resolution,
        'status': status,
        'fix_version': fixVersion,
        'start': cardStart,
        'end': cardEnd,
        'project': project,
        'security': security,
        'card_type': card_type
    }

    log.debug("Default values: {0}".format(defaults))

    card, created = Card.objects.get_or_create(
        key=issue.key, defaults=defaults)
    defaults.update({'components': components})

    if options[JIRA_IMPLEMENTS]:
        defaults.update({'implementedby': implementedby_list})
    if options[JIRA_DEPENDSON]:
        defaults.update({'dependson': depends_list})
    defaults.update({'labels': label_list})

    if not created:
        for attr, value in defaults.iteritems():
            attribute = getattr(card, attr)
            if isinstance(card._meta.get_field_by_name(attr)[0],
                          ManyToManyField):
                if set([x.pk for x in attribute.all()]) != set(value):
                    log.debug("{0} old: {1}, new: {2}".format(
                        attr, [x.pk for x in attribute.all()], value))
                    setattr(card, attr, value)
            else:
                if attribute != value:
                    log.debug("{0} old: {1}, new: {2}".format(
                        attr, getattr(card, attr), value))
                    setattr(card, attr, value)
    else:
        card.components = components
        if options[JIRA_IMPLEMENTS]:
            card.implementedby = implementedby_list
        if options[JIRA_DEPENDSON]:
            card.dependson = depends_list
        card.labels = label_list

    log.info("Saving card {0}".format(issue.key))
    card.save()
    log.debug(u"Saved {0} - {1}".format(issue.key, summary))

    return card


def get_card_blueprints(card):
    blueprint_type = CardType.objects.get(name="Blueprint")
    blueprints = []
    for c in card.implementedby.all():
        if c.card_type == blueprint_type:
            blueprints.append(c)
            log.debug("{0} - {1}".format(c.key, c.status.name))
        else:
            blueprints.extend(get_card_blueprints(c))
    return blueprints


def get_component_blueprints(component, snapshot_date):
    blueprint_type = CardType.objects.get(name="Blueprint")
    blueprints = []
    from_milestone = Milestone.objects.filter(
        date__lte=snapshot_date,
        is_major=True).order_by("-date")[0]
    start_date = from_milestone.date
    to_milestone = Milestone.objects.filter(
        date__gt=snapshot_date,
        is_major=True).order_by("date")[0]
    end_date = to_milestone.date
    for card in component.card_set.filter(
            fix_version__fix_date__gt=start_date,
            fix_version__fix_date__lt=end_date):

        log.debug("{0}".format(card.key))
        if card.card_type == blueprint_type:
            blueprints.append(card)
        else:
            blueprints.extend(get_card_blueprints(card))
    return blueprints


def collect_component_burndown(project):
    components = Component.objects.filter(project=project)

    for component in components:
        log.debug("Processing component {0}".format(component))
        snapshot_date = timezone.make_aware(
            datetime.now(),
            timezone.get_default_timezone())

        blueprints = get_component_blueprints(component, snapshot_date)
        burndown, created = Burndown.objects.get_or_create(component=component)
        snapshot = BurndownSnapshot(burndown=burndown, date=snapshot_date)
        snapshot.save()

        for name in settings.JIRA_STATUSES:
            log.debug("Analyzing status {0}".format(name))
            bbar = BurndownBar(snapshot=snapshot, name=name, value=0)

            for bp in blueprints:
                if bp.status.name == name:
                    log.debug("Blueprint with status {0}: {1}".format(
                        name, bp.key))
                    bbar.value += 1
            bbar.save()


def collect_burndown(project, card_type):
    snapshot_date = timezone.make_aware(
        datetime.now(),
        timezone.get_default_timezone())

    blueprint_type = CardType.objects.get(name="Blueprint")
    from_milestone = Milestone.objects.filter(
        date__lte=snapshot_date,
        is_major=True).order_by("-date")[0]
    start_date = from_milestone.date
    to_milestone = Milestone.objects.filter(
        date__gt=snapshot_date,
        is_major=True).order_by("date")[0]
    end_date = to_milestone.date
    cards = Card.objects.filter(
        project=project,
        fix_version__fix_date__gt=start_date,
        fix_version__fix_date__lt=end_date)

    blueprints = []
    for card in cards:
        if card.card_type == blueprint_type:
            blueprints.append(card)
        else:
            blueprints.extend(get_card_blueprints(card))

    burndown, created = Burndown.objects.get_or_create(project=project)
    snapshot = BurndownSnapshot(burndown=burndown, date=snapshot_date)
    snapshot.save()

    for name in settings.JIRA_STATUSES:
        log.debug("Analyzing status {0}".format(name))

        bbar = BurndownBar(snapshot=snapshot, name=name, value=0)
        for bp in blueprints:
            if bp.status.name == name:
                log.debug("Blueprint with status {0}: {1}".format(
                    name, bp.key))
                bbar.value += 1
        bbar.save()
