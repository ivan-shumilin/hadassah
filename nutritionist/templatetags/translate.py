from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def translate(words):
    dictionary = {
        'breakfast': 'завтрак',
        'lunch': 'обед',
        'afternoon': 'полдник',
        'dinner': 'ужин',
        'salad': 'салат',
        'soup': 'суп',
        'main': 'основное блюдо',
        'garnish': 'гарнир'
    }
    return dictionary.get(words, "")