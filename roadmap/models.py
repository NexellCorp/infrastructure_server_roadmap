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

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from reversion.models import Revision


class CardAggregateModel(models.Model):
    def aggregate(self, **kwargs):
        cardset = self.card_set.all()
        if 'aggrby' in kwargs.keys() and 'aggrbyname' in kwargs.keys():
            cardset = cardset.filter(
                **{kwargs['aggrbyname']: kwargs['aggrby']})
        if 'from' in kwargs.keys():
            cardset = cardset.filter(fix_version__fix_date__gt=kwargs['from'].date)
        if 'to' in kwargs.keys():
            cardset = cardset.filter(fix_version__fix_date__lt=kwargs['to'].date)
        return cardset.count()

    class Meta:
        abstract = True


# XXX: Should be moved to separate application
class Burndown(models.Model):
    project = models.ForeignKey('Project', null=True, blank=True)
    component = models.ForeignKey('Component', null=True, blank=True)

    def __unicode__(self):
        ret_val = self.pk
        if self.component:
            ret_val = self.component.name
        return ret_val


class BurndownSnapshot(models.Model):
    burndown = models.ForeignKey('Burndown')
    date = models.DateTimeField()

    def __unicode__(self):
        return "%s - %s" % (str(self.burndown), str(self.date))


class BurndownBar(models.Model):
    snapshot = models.ForeignKey('BurndownSnapshot')
    name = models.CharField(max_length=32)
    value = models.IntegerField()

    def __unicode__(self):
        return "%s - %s" % (str(self.snapshot), self.name)
# end of burndown


class CardType(models.Model):
    name = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class Milestone(models.Model):
    name = models.CharField(max_length=128)
    date = models.DateTimeField()
    is_major = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def is_from_selected(self):
        milestones = Milestone.objects.filter(is_major=True).order_by("date")
        if self == milestones[milestones.count() - 2]:
            return True
        return False

    def is_to_selected(self):
        milestones = Milestone.objects.filter(is_major=True).order_by("date")
        if self == milestones[milestones.count() - 1]:
            return True
        return False


class SecurityLevel(models.Model):
    name = models.CharField(max_length=128)
    login_mandatory = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name


class Project(CardAggregateModel):
    name = models.CharField(max_length=128)
    key = models.CharField(max_length=32)

    def __unicode__(self):
        return self.name


class RoadmapRelease(models.Model):
    revision = models.OneToOneField(Revision)  # This is required
    date = models.DateTimeField(auto_now_add=True)
    release_name = models.CharField(validators=[
        RegexValidator(
            r'[1-9][0-9]{3}-[0-9]{2}',
            'Version syntax YYYY-MM',
            'Invalid version'
        ),
    ], max_length=7)

    def __unicode__(self):
        return self.release_name


class FixVersion(models.Model):
    name = models.CharField(max_length=32)
    fix_date = models.DateTimeField()
    project = models.ForeignKey('Project', blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.project.name)


class Resolution(models.Model):
    name = models.CharField(max_length=32)
    project = models.ForeignKey('Project', blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.project.name)


class StatusStyle(models.Model):
    class_name = models.CharField(max_length=64)
    color = models.CharField(validators=[
        RegexValidator(
            r'#[0-9a-fA-F]{6}',
            'Version syntax #XXXXXX where X is hex number 0-F',
            'Invalid version'
        ),
    ], max_length=7)

    def __unicode__(self):
        return self.class_name


class Status(CardAggregateModel):
    name = models.CharField(max_length=32)
    status_style = models.ForeignKey('StatusStyle', blank=True, null=True)
    project = models.ForeignKey('Project', blank=True, null=True)
    display_order = models.IntegerField(blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.name)

    @property
    def style(self):
        if self.name == "Drafting":
            return "concept"
        if self.name == "Review":
            return "approved"
        if self.name == "Planning":
            return "planning"
        if self.name == "Engineering":
            return "development"
        if self.name == "In Progress":
            return "development"
        if self.name == "Change Review":
            return "development"
        if self.name == "Resolved":
            return "released"
        if self.name == "Closed":
            return "released"
        if self.name == "Closing-review":
            return "released"


class Component(CardAggregateModel):
    name = models.CharField(max_length=128)
    project = models.ForeignKey(
        'Project',
        related_name="component_set")
    engineering_project = models.OneToOneField(
        'Project',
        related_name="engineering_component",
        blank=True,
        null=True)

    def __unicode__(self):
        return "%s - %s" % (self.name, self.project.name)


class Label(models.Model):
    name = models.CharField(max_length=128)

    def __unicode__(self):
        return self.name


class Card(models.Model):
    ONGOING = "ONGOING"
    FIXDATE = "FixDate"
    key = models.CharField(max_length=128, primary_key=True)
    url = models.URLField()
    summary = models.TextField()
    components = models.ManyToManyField('Component', null=True, blank=True)
    status = models.ForeignKey('Status')
    resolution = models.ForeignKey('Resolution', null=True, blank=True)
    fix_version = models.ForeignKey('FixVersion', null=True, blank=True)

    # for ongoing cards only
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)

    implementedby = models.ManyToManyField(
        "self", related_name="implements", symmetrical=False)
    dependson = models.ManyToManyField(
        "self", related_name="depends", symmetrical=False)
    labels = models.ManyToManyField('Label', null=True, blank=True)
    project = models.ForeignKey('Project')
    security = models.ForeignKey('SecurityLevel', blank=True, null=True)
    card_type = models.ForeignKey('CardType')

    def __unicode__(self):
        return self.key

    def aggregate(self, **kwargs):
        cardset = self.implementedby.all()
        if 'aggrby' in kwargs.keys() and 'aggrbyname' in kwargs.keys():
            cardset = cardset.filter(
                **{kwargs['aggrbyname']: kwargs['aggrby']})
        if 'from' in kwargs.keys():
            cardset = cardset.filter(start__gt=kwargs['from'].date)
        if 'to' in kwargs.keys():
            cardset = cardset.filter(start__lt=kwargs['to'].date)
        return cardset.count()

    @property
    def is_valid_swimlane(self):
        if self.is_toplevel and not self.resolution:
            return True
        return False

    @property
    def is_valid(self):
        if self.event_type == self.FIXDATE and self.fix_version is None:
            return False
        if self.event_type == self.ONGOING and self.start is None:
            return False
        if self.resolution and self.resolution.name == "Cancelled":
            return False
        if self.status.name == settings.UPSTREAM_DEVELOPMENT and self.end is None:
            return False
        return True

    @property
    def is_v7(self):
        if self.labels.filter(name="ARMv7-A"):
            return True
        return False

    @property
    def is_v8(self):
        if self.labels.filter(name="ARMv8-A"):
            return True
        return False

    @property
    def is_epic(self):
        if self.summary.startswith("EPIC") and \
           self.labels.filter(name="EPIC") and \
           self.event_type == self.ONGOING:
            return True
        return False

    @property
    def is_toplevel(self):
        if not self.implements.all():
            return True
        return False

    @property
    def event_type(self):
        if self.fix_version.name == self.ONGOING:
            return self.ONGOING
        if self.status.name == settings.UPSTREAM_DEVELOPMENT:
            return self.ONGOING
        return self.FIXDATE

    @property
    def start_date(self):
        if self.event_type == self.ONGOING:
            return self.start
        return self.fix_version.fix_date

    @property
    def end_date(self):
        if self.event_type == self.ONGOING and self.end:
            return self.end
        return None

    @property
    def style(self):
        return self.status.status_style.class_name
