from django import template
from django.db.models import fields

register = template.Library()

class CardDiff(template.Node):
    def __init__(self, prev, new):
        self.prev = template.Variable(prev)
        self.new = template.Variable(new)
    def render(self, context):
        prev = self.prev.resolve(context)
        new = self.new.resolve(context)
        ret = "<tr><td><a href=\"%s\">%s - %s</a></td><td><a href=\"%s\">%s - %s</a></td></tr>" % (prev.url, prev.status.name, prev.summary,
             new.url, new.status.name, new.summary)
        #ret += "<tr><td colspan=\"2\"><table width=\"100%\" border=\"1\">"
        for field in prev._meta.fields:
            if field.value_from_object(prev) != field.value_from_object(new):
                if not isinstance(field, fields.related.RelatedField):
                    ret += "<tr><td>%s - %s</td><td>%s - %s</td></tr>" % (field.verbose_name, field.value_from_object(prev), field.verbose_name, field.value_from_object(new))
                else: 
                    prev_pk = field.value_from_object(prev)
                    try:
                        prev_val = field.related.parent_model.objects.get(pk=prev_pk)
                    except field.related.parent_model.DoesNotExist:
                        prev_val = None 
                    new_pk = field.value_from_object(new)
                    try:
                        new_val = field.related.parent_model.objects.get(pk=new_pk)
                    except field.related.parent_model.DoesNotExist:
                        new_val = None
                    ret += "<tr><td>%s - %s</td><td>%s - %s</td></tr>" % (field.verbose_name, prev_val, field.verbose_name, new_val)
        #ret += "</table></td></tr>"
            
        return ret

@register.tag(name="card_diff")
def do_current_time(parser, token):
    try:
        # split_contents() knows not to split quoted strings.
        tag_name, prev, new = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError("%r tag requires 2 arguments" % token.contents.split()[0])
    return CardDiff(prev, new)

