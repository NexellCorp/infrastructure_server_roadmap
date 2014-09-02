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

from django import template
from django.utils.encoding import smart_str

register = template.Library()


def parse_args_kwargs_and_as_var(parser, bits):

    args = []
    kwargs = {}
    as_var = None

    bits = iter(bits)
    for bit in bits:
        if bit == 'as':
            as_var = bits.next()
            break
        else:
            for arg in bit.split(","):
                if '=' in arg:
                    k, v = arg.split('=', 1)
                    k = k.strip()
                    kwargs[k] = parser.compile_filter(v)
                elif arg:
                    args.append(parser.compile_filter(arg))
    return args, kwargs, as_var


def get_args_and_kwargs(args, kwargs, context):
    out_args = [arg.resolve(context) for arg in args]
    out_kwargs = dict([(smart_str(k, 'ascii'), v.resolve(context))
                      for k, v in kwargs.items()])
    return out_args, out_kwargs


class CardAggregate(template.Node):

    def __init__(self, args, kwargs, as_var):
        self.args = args
        self.kwargs = kwargs
        self.as_var = as_var

    def render(self, context):

        args, kwargs = get_args_and_kwargs(self.args, self.kwargs, context)

        # call something with the args or kwargs here
        if hasattr(args[0], 'aggregate'):
            return args[0].aggregate(**kwargs)

        return ''


@register.tag(name="card_aggregate")
def do_card_aggregate(parser, token):
    bits = token.contents.split(' ')
    if len(bits) < 1:
        raise template.TemplateSyntaxError(
            "'%s' takes at least one argument" % bits[0])

    if len(bits) > 1:
        args, kwargs, as_var = parse_args_kwargs_and_as_var(parser, bits[1:])

    return CardAggregate(args, kwargs, as_var)
