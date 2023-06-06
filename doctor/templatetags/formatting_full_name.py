from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def formatting_full_name(full_name):
    list = full_name.split()
    res = ''
    for index, value in enumerate(list):
        if index == 0:
            res += value.capitalize() + ' '
            continue
        if index == len(list) - 1:
            res += value[0:1].capitalize() + '.'
            continue
        else:
            res += value[0:1].capitalize() + '.'
    return res.strip()