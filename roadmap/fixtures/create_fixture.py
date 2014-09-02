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

import yaml
import parsedatetime.parsedatetime as pdt

from dateutil import rrule
from datetime import datetime, timedelta


def create_milestone(index, milestone_name, milestone_date, is_major=False):
    return {'model': 'roadmap.Milestone',
         'pk': index,
         'fields':
              {'name': milestone_name,
               'date': milestone_date.strftime("%Y-%m-%d"),
               'is_major': is_major,
              }
        }

c = pdt.Constants(usePyICU=False)
c.BirthdayEpoch = 80
p = pdt.Calendar(c)

start = datetime.strptime("2011-01-01", "%Y-%m-%d")
end = datetime.strptime("2015-12-31", "%Y-%m-%d")

initial_data = []
last_index = 0
for index, dt in enumerate(
    rrule.rrule(rrule.MONTHLY, dtstart=start, until=end),
    start=1):
    dtstring = "last thursday of %s" % dt.strftime("%B %Y")
    milestone_name = dt.strftime("%Y.%m")
    print dtstring
    milestone_date = datetime(*p.parseDateText(dtstring)[:6])
    initial_data.append(
        create_milestone(index, milestone_name, milestone_date, False))
    last_index = index

last_index = last_index + 1
milestone_name = "Linaro Connect Europe/UDS 2011"
milestone_date = datetime(*p.parseDateText("9th May 2011")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

last_index = last_index + 1
milestone_name = "Linaro Connect Europe 2011"
milestone_date = datetime(*p.parseDateText("1st August 2011")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

last_index = last_index + 1
milestone_name = "Linaro Connect USA 2011"
milestone_date = datetime(*p.parseDateText("31st October 2011")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

last_index = last_index + 1
milestone_name = "Linaro Connect USA 2012"
milestone_date = datetime(*p.parseDateText("6th February 2012")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

last_index = last_index + 1
milestone_name = "Linaro Connect Asia 2012"
milestone_date = datetime(*p.parseDateText("28th May 2012")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

last_index = last_index + 1
milestone_name = "Linaro Connect Europe 2013"
milestone_date = datetime(*p.parseDateText("8th July 2013")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

last_index = last_index + 1
milestone_name = "Linaro Connect Asia 2013"
milestone_date = datetime(*p.parseDateText("4th March 2013")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

last_index = last_index + 1
milestone_name = "Linaro Connect Europe 2012"
milestone_date = datetime(*p.parseDateText("29th October 2012")[:6])
initial_data.append(
    create_milestone(last_index, milestone_name, milestone_date, True))

f = open("initial_data.yaml", "w")
f.write(yaml.dump(initial_data))
f.close()
