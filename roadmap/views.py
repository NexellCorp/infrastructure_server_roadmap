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

import json
import sys
import traceback

from datetime import (
    datetime,
    timedelta,
)

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models import Max, Min
from django.http import HttpResponse, HttpResponseServerError
from django.template import RequestContext, loader
from django.views.decorators.csrf import csrf_exempt

from roadmap.forms import LabelForm
from roadmap.helpers import (
    DEBUG,
    SINGLE_UPDATE,
    JIRA_SERVER,
    JIRA_IMPLEMENTS,
    JIRA_DEPENDSON,
    create_or_update
)
from roadmap.models import (
    BurndownSnapshot,
    Card,
    Component,
    Status,
    Project,
    Resolution,
    Label,
    Milestone,
)


@login_required
def index(request):
    major_milestones = Milestone.objects.filter(is_major=True).order_by("date")
    from_milestone = major_milestones.filter(
        date__lte=datetime.now()).order_by("-date")[0]
    to_milestone = major_milestones.filter(date__gt=datetime.now())[0]

    # leave this section for now although should not be used from UI
    if (request.GET and 'from' in request.GET.keys()
            and 'end' in request.GET.keys()):
        from_milestone = Milestone.objects.get(pk=request.GET['from'])
        to_milestone = Milestone.objects.get(pk=request.GET['end'])

    template = loader.get_template('roadmap/index.html')
    project = Project.objects.get(name=settings.JIRA_PROJECT)

    days_between_milestones = (to_milestone.date - from_milestone.date).days
    burndown_snapshots = BurndownSnapshot.objects.filter(
        burndown__project=project,
        date__lt=to_milestone.date,
        date__gt=from_milestone.date)
    burndown_categories = []
    burndown_meta_series = {}
    bar_names = set([])
    burndown_series = {}
    total_max = 0
    # for now there is a silent assumption that the projects share the
    # blueprint statuses
    #bars_max = 0
    for snapshot in burndown_snapshots.all():
        total = 0
        #if bars_max < snapshot.burndownbar_set.count():
        #    bars_max = snapshot.burndownbar_set.count()
        burndown_meta_series[snapshot.date.strftime("%Y-%m-%d")] = {}
        for bar in snapshot.burndownbar_set.all():
            total = total + bar.value
            bar_names.add(bar.name)
            burndown_meta_series[
                snapshot.date.strftime("%Y-%m-%d")][bar.name] = bar.value
        if total > total_max:
            total_max = total

    # snapshots are assumed to be taken daily
    for name in bar_names:
        burndown_series[name] = []

    for date in [from_milestone.date + timedelta(days=x)
                 for x in range(0, days_between_milestones)]:
        date_key = date.strftime("%Y-%m-%d")
        burndown_categories.append(date_key)

        if date_key in burndown_meta_series:
            for key in burndown_meta_series[date_key].keys():
                burndown_series[key].append(
                    burndown_meta_series[date_key][key])
        else:
            for key in burndown_series.keys():
                burndown_series[key].append(0)

    burndown_line = []
    if days_between_milestones > 0:
        a = float(-(float(total_max) / float(days_between_milestones)))
        for point in range(0, days_between_milestones):
            value = a * point + total_max
            burndown_line.append(value)

    tick_interval = 10
    if days_between_milestones > 20:
        tick_interval = days_between_milestones / 10

    display_burndown_series = []
    for serie_name in settings.JIRA_STATUSES:
        if serie_name in burndown_series:
            display_burndown_series.append(
                (serie_name, burndown_series[serie_name]))

    components = Component.objects.filter(project=project).order_by("name")
    statuses = Status.objects.filter(project=project).order_by("display_order")
    context = RequestContext(request, {
        'project': project,
        'components': components,
        'statuses': statuses,
        'from_milestone': from_milestone,
        'to_milestone': to_milestone,
        'burndown_categories': burndown_categories,
        'burndown_series': display_burndown_series,
        'burndown_line': burndown_line,
        'tick_interval': tick_interval,
    })
    return HttpResponse(template.render(context))


@login_required
def component(request, roadmap_id):
    major_milestones = Milestone.objects.filter(is_major=True).order_by("date")
    from_milestone = major_milestones.filter(
        date__lte=datetime.now()).order_by("-date")[0]
    to_milestone = major_milestones.filter(date__gt=datetime.now())[0]
    component = Component.objects.get(pk=roadmap_id)
    statuses = Status.objects.filter(
        project=component.project).order_by("display_order")

    # leave this section for now although should not be used from UI
    if (request.GET and 'from' in request.GET.keys()
            and 'end' in request.GET.keys()):
        from_milestone = Milestone.objects.get(pk=request.GET['from'])
        to_milestone = Milestone.objects.get(pk=request.GET['end'])

    if request.GET and 'status' in request.GET.keys():
        statuses = Status.objects.filter(pk__in=[request.GET['status']])

    template = loader.get_template('roadmap/component.html')

    days_between_milestones = (to_milestone.date - from_milestone.date).days
    burndown_snapshots = BurndownSnapshot.objects.filter(
        burndown__component=component,
        date__lt=to_milestone.date,
        date__gt=from_milestone.date)
    burndown_categories = []
    burndown_meta_series = {}
    bar_names = set([])
    burndown_series = {}
    total_max = 0
    # for now there is a silent assumption that the projects share
    # the blueprint statuses
    #bars_max = 0
    for snapshot in burndown_snapshots.all():
        total = 0
        #if bars_max < snapshot.burndownbar_set.count():
        #    bars_max = snapshot.burndownbar_set.count()
        burndown_meta_series[snapshot.date.strftime("%Y-%m-%d")] = {}
        for bar in snapshot.burndownbar_set.all():
            total = total + bar.value
            bar_names.add(bar.name)
            burndown_meta_series[
                snapshot.date.strftime("%Y-%m-%d")][bar.name] = bar.value
        if total > total_max:
            total_max = total

    # snapshots are assumed to be taken daily
    for name in bar_names:
        burndown_series[name] = []

    for date in [from_milestone.date + timedelta(days=x)
                 for x in range(0, days_between_milestones)]:
        date_key = date.strftime("%Y-%m-%d")
        burndown_categories.append(date_key)
        if date_key in burndown_meta_series:
            for key in burndown_meta_series[date_key].keys():
                burndown_series[key].append(
                    burndown_meta_series[date_key][key])
        else:
            for key in burndown_series.keys():
                burndown_series[key].append(0)

    burndown_line = []
    if days_between_milestones > 0:
        a = float(-(float(total_max) / float(days_between_milestones)))
        for point in range(0, days_between_milestones):
            value = a * point + total_max
            burndown_line.append(value)

    display_burndown_series = []
    for serie_name in settings.JIRA_STATUSES:
        if serie_name in burndown_series:
            display_burndown_series.append(
                (serie_name, burndown_series[serie_name]))

    tick_interval = 10
    if days_between_milestones > 20:
        tick_interval = days_between_milestones / 10

    roadmap_cards = Card.objects.filter(
        components__in=[component],
        fix_version__fix_date__lt=to_milestone.date,
        fix_version__fix_date__gt=from_milestone.date,
        status__in=statuses)
    # statuses = Status.objects.filter(project=component.project).
    # order_by("display_order")
    context = RequestContext(request, {
        'component': component,
        'statuses': statuses,
        'roadmap_cards': roadmap_cards,
        'from_milestone': from_milestone,
        'to_milestone': to_milestone,
        'burndown_categories': burndown_categories,
        'burndown_series': display_burndown_series,
        'burndown_line': burndown_line,
        'tick_interval': tick_interval,
    })
    return HttpResponse(template.render(context))


@login_required
def status(request, status_id):
    major_milestones = Milestone.objects.filter(is_major=True).order_by("date")
    from_milestone = major_milestones.filter(
        date__lte=datetime.now()).order_by("-date")[0]
    to_milestone = major_milestones.filter(date__gt=datetime.now())[0]
    status = Status.objects.get(pk=status_id)
    components = Component.objects.filter(project=status.project)
    roadmap_cards = Card.objects.filter(
        components__in=components,
        start__lt=to_milestone.date,
        start__gt=from_milestone.date,
        status=status)

    template = loader.get_template('roadmap/status.html')
    context = RequestContext(request, {
        'components': components,
        'status': status,
        'roadmap_cards': roadmap_cards,
        'from_milestone': from_milestone,
        'to_milestone': to_milestone,
    })
    return HttpResponse(template.render(context))


@login_required
def search(request):
    if request.GET and 'label' in request.GET.keys():
        form = LabelForm(request.GET)
        if form.is_valid():
            label = Label.objects.filter(
                name__iexact=form.cleaned_data['label'])
            cards = None
            if label:
                invalid_resolutions = Resolution.objects.filter(
                    project__name=settings.JIRA_PROJECT, 
                    name__in=settings.JIRA_INVALID_RESOLUTIONS)
                cards = Card.objects.filter(
                    labels__in=label,
                    project__name=settings.JIRA_PROJECT).exclude(
                        resolution__in=invalid_resolutions)
            if not cards or cards.count() == 0:
                context = RequestContext(request, {
                    'form': form,
                    })
                template = loader.get_template('roadmap/search.html')
                return HttpResponse(template.render(context))
               
            components = Component.objects.filter(
                project__name=settings.JIRA_PROJECT).order_by("name")
            for component in components:
                if cards.filter(components__in=[component]).count() == 0:
                    components = components.exclude(pk=component.pk)

            roadmap_start = min(
                [cards.aggregate(Min("start")).items()[0][1],
                 cards.exclude(fix_version__name="ONGOING").aggregate(
                     Min("fix_version__fix_date")).items()[0][1]])
            # labels are on the right, so 2 months leading time line is enough
            roadmap_start = roadmap_start - timedelta(days=60)
            roadmap_end = max(
                [cards.aggregate(Max("start")).items()[0][1],
                 cards.exclude(fix_version__name="ONGOING").aggregate(
                     Max("fix_version__fix_date")).items()[0][1]])
            roadmap_end = roadmap_end + timedelta(days=180)
            context = RequestContext(request, {
                'cards': cards,
                'components': components,
                'roadmap_start': roadmap_start,
                'roadmap_end': roadmap_end,
                })
            template = loader.get_template('roadmap/timeline.html')
            return HttpResponse(template.render(context))
        else:
            context = RequestContext(request, {
                'form': form,
                })
            template = loader.get_template('roadmap/search.html')
            return HttpResponse(template.render(context))

    label_search_form = LabelForm()
    context = RequestContext(request, {
        'form': label_search_form,
        })
    template = loader.get_template('roadmap/search.html')
    return HttpResponse(template.render(context))


@login_required
def roadmap(request, roadmap_id):
    components = Component.objects.filter(
        project__name=settings.JIRA_PROJECT).order_by("name")
    current_roadmap = Component.objects.get(pk=roadmap_id)
    invalid_resolutions = Resolution.objects.filter(
        project=current_roadmap.project, 
        name__in=settings.JIRA_INVALID_RESOLUTIONS)
    roadmap_cards = current_roadmap.card_set.all().exclude(
        resolution__in=invalid_resolutions)
    epics = roadmap_cards.filter(
        # labels__name__contains="EPIC",
        summary__startswith="EPIC",
        implements=None,
        resolution=None
    )
    other_cards = roadmap_cards.exclude(pk__in=epics).filter(implements=None)

    non_epics = roadmap_cards.exclude(pk__in=epics)
    roadmap_start = min(
        [non_epics.aggregate(Min("start")).items()[0][1],
         non_epics.exclude(fix_version__name="ONGOING").aggregate(
             Min("fix_version__fix_date")).items()[0][1]])
    # labels are on the right, so 2 months leading time line is enough
    if roadmap_start:
        roadmap_start = roadmap_start - timedelta(days=60)

    roadmap_end = max(
        [non_epics.aggregate(Max("start")).items()[0][1],
         non_epics.exclude(fix_version__name="ONGOING").aggregate(
             Max("fix_version__fix_date")).items()[0][1]])
    if roadmap_end:
        roadmap_end = roadmap_end + timedelta(days=180)
    template = loader.get_template('roadmap/roadmap.html')
    context = RequestContext(request, {
        'current': current_roadmap,
        'components': components,
        'cards': roadmap_cards,
        'other_cards': other_cards,
        'epics': epics,
        'roadmap_start': roadmap_start,
        'roadmap_end': roadmap_end,
    })
    return HttpResponse(template.render(context))


@csrf_exempt
def update_card(request):
    if (request.method == "POST"
            and request.META['REMOTE_ADDR'] in settings.TRUSTED_ADDRESS):
        card_json = json.loads(request.body)
        jira_server_parts = card_json['issue']['self'].split("/")
        options = {
            DEBUG: settings.DEBUG,
            JIRA_SERVER: jira_server_parts[0] + "//" + jira_server_parts[2],
            JIRA_IMPLEMENTS: True,
            JIRA_DEPENDSON: True,
            SINGLE_UPDATE: True
        }
        try:
            create_or_update(card_json['issue'], options, None)
        except:
            print sys.exc_info()[0]
            print traceback.format_exc()

            return HttpResponseServerError()
    return HttpResponse()


@login_required
def roadmap_index(request):
    template = loader.get_template('roadmap/roadmap_index.html')

    project = Project.objects.get(name=settings.JIRA_PROJECT)
    components = Component.objects.filter(project=project).order_by("name")

    context = RequestContext(request, {
        'project': project,
        'components': components,
    })

    return HttpResponse(template.render(context))
