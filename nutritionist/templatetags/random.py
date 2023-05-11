from django import template
from django.template.defaultfilters import stringfilter
from random import randint

register = template.Library()

@register.filter
@stringfilter
def random(url):
    return f'{url}?v={str(randint(1, 10000))}'