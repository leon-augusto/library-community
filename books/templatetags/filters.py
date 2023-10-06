from django import template
from datetime import datetime

register = template.Library()


@register.filter
def show_time(value1, value2):
    if all((isinstance(value1, datetime), isinstance(value2, datetime))):
        return (value1 - value2).days
    else:
        return 'It does not return it yet.'
