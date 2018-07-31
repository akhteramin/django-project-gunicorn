from django import template
import json

register = template.Library()

@register.filter
def get_json(value,arg):
    # timestamp = "2008-09-26T01:51:42.000Z"
    return json.dumps(value)