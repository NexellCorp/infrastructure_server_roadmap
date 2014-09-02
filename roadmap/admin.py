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

from django.contrib import admin
from roadmap.models import (
    FixVersion,
    StatusStyle,
    Status,
    Card,
    CardType,
    Component,
    Project,
    Resolution,
    RoadmapRelease,
    Milestone
)
import reversion


class CardAdmin(reversion.VersionAdmin):
    pass


class CardTypeAdmin(reversion.VersionAdmin):
    pass


class StatusAdmin(reversion.VersionAdmin):
    pass


class FixVersionAdmin(reversion.VersionAdmin):
    pass


class StatusStyleAdmin(reversion.VersionAdmin):
    pass


class ComponentAdmin(reversion.VersionAdmin):
    pass


class ResolutionAdmin(reversion.VersionAdmin):
    pass


class ProjectAdmin(reversion.VersionAdmin):
    pass


class MilestoneAdmin(reversion.VersionAdmin):
    pass

admin.site.register(FixVersion, FixVersionAdmin)
admin.site.register(StatusStyle, StatusStyleAdmin)
admin.site.register(Status, StatusAdmin)
admin.site.register(Card, CardAdmin)
admin.site.register(CardType, CardTypeAdmin)
admin.site.register(Component, ComponentAdmin)
admin.site.register(Resolution, ResolutionAdmin)
admin.site.register(RoadmapRelease)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Milestone, MilestoneAdmin)
