from django import template
from datetime import datetime

register = template.Library()

@register.filter
def get_date_time(value, arg):
    return datetime.fromtimestamp((int(value)+(6*3600*1000))/1000.0)

@register.filter
def is_today(a_date):
    a_date = datetime.fromtimestamp((int(a_date) + (6 * 3600 * 1000)) / 1000.0)

    print((datetime.now()-a_date).days)
    return (datetime.now()-a_date).days == 0